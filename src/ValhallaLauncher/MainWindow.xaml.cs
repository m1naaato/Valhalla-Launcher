using System;
using System.Diagnostics;
using System.IO;
using System.IO.Compression;
using System.Linq;
using System.Net.Http;
using System.Security.Cryptography;
using System.Text.Json;
using System.Threading.Tasks;
using System.Windows;

namespace ValhallaLauncher;

public partial class MainWindow : Window
{
    readonly HttpClient http = new();
    LauncherConfig cfg = new();
    string? prismPath;
    bool launching;
    bool uiReady;

    string UserCfg => Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData), "Valhalla", "settings.json");

    public MainWindow()
    {
        InitializeComponent();
        uiReady = true;
        LoadConfig();
        prismPath = FindPrism();
        LoadSettings();
        Refresh();
        Loaded += async (_, _) =>
        {
            await LoadRemoteConfig();
            await CheckLauncherUpdate(false);
        };
    }

    void ShowPage(UIElement page)
    {
        HomePage.Visibility = Visibility.Collapsed;
        ModpackPage.Visibility = Visibility.Collapsed;
        SettingsPage.Visibility = Visibility.Collapsed;
        page.Visibility = Visibility.Visible;
    }

    void Accueil_Click(object s, RoutedEventArgs e) => ShowPage(HomePage);
    void Modpack_Click(object s, RoutedEventArgs e) => ShowPage(ModpackPage);
    void Parametres_Click(object s, RoutedEventArgs e) => ShowPage(SettingsPage);

    void Compte_Click(object s, RoutedEventArgs e)
    {
        MessageBox.Show(
            "La connexion Microsoft intégrée n'est pas encore activée dans cette version. Valhalla ne demande ni ne stocke ton mot de passe Microsoft.",
            "Valhalla - Compte Minecraft",
            MessageBoxButton.OK,
            MessageBoxImage.Information);
    }

    void CopyIp_Click(object s, RoutedEventArgs e)
    {
        try
        {
            Clipboard.SetText(cfg.Server);
            StatusText.Text = "✓ Adresse du serveur copiée";
        }
        catch (Exception ex)
        {
            StatusText.Text = "Copie impossible : " + ex.Message;
        }
    }

    void LoadConfig()
    {
        try
        {
            var p = Path.Combine(AppContext.BaseDirectory, "config.json");
            if (File.Exists(p))
                cfg = JsonSerializer.Deserialize<LauncherConfig>(File.ReadAllText(p), new JsonSerializerOptions { PropertyNameCaseInsensitive = true }) ?? new();
        }
        catch { }
    }

    void LoadSettings()
    {
        try
        {
            if (!File.Exists(UserCfg)) return;
            var s = JsonSerializer.Deserialize<UserSettings>(File.ReadAllText(UserCfg));
            if (s == null) return;
            RamSlider.Value = Math.Clamp(s.RamMb / 1024.0, 4, 16);
            RamValueText.Text = $"{(int)RamSlider.Value} Go";
            DirectConnectCheck.IsChecked = s.DirectConnect;
        }
        catch { }
    }

    void SaveSettings()
    {
        if (!uiReady || RamSlider == null || DirectConnectCheck == null || StatusText == null) return;
        try
        {
            var ram = (int)RamSlider.Value * 1024;
            Directory.CreateDirectory(Path.GetDirectoryName(UserCfg)!);
            File.WriteAllText(UserCfg, JsonSerializer.Serialize(
                new UserSettings { RamMb = ram, DirectConnect = DirectConnectCheck.IsChecked == true },
                new JsonSerializerOptions { WriteIndented = true }));
            StatusText.Text = "✓ Paramètres enregistrés";
        }
        catch (Exception ex)
        {
            StatusText.Text = "Erreur paramètres : " + ex.Message;
        }
    }

    void Refresh()
    {
        HomePackText.Text = $"{cfg.ModpackName} • Minecraft {cfg.MinecraftVersion}";
        PackNameText.Text = cfg.ModpackName;
        PackInfoText.Text = $"Minecraft {cfg.MinecraftVersion} • {cfg.Loader} • pack {cfg.PackVersion}";
        ServerStatusText.Text = string.IsNullOrWhiteSpace(cfg.Server) ? "Serveur : non configuré" : "Serveur : configuré";
        StatusText.Text = prismPath == null ? "Configuration Minecraft requise" : "✓ Moteur Minecraft prêt";
    }

    string? FindPrism()
    {
        string[] c =
        {
            Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData), "Programs", "PrismLauncher", "prismlauncher.exe"),
            Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ProgramFiles), "PrismLauncher", "prismlauncher.exe"),
            Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ProgramFilesX86), "PrismLauncher", "prismlauncher.exe")
        };
        return c.FirstOrDefault(File.Exists);
    }

    void Prepare_Click(object s, RoutedEventArgs e)
    {
        prismPath = FindPrism();
        if (prismPath == null)
        {
            StatusText.Text = "Installation du moteur Minecraft requise.";
            MessageBox.Show(
                "Prism Launcher doit être installé une fois comme moteur Minecraft. Il restera utilisé en arrière-plan.",
                "Valhalla - Préparation",
                MessageBoxButton.OK,
                MessageBoxImage.Information);
            return;
        }

        InstallInstanceSilently();
        StatusText.Text = "✓ Modpack préparé";
    }

    void InstallInstanceSilently()
    {
        try
        {
            var archive = Path.Combine(AppContext.BaseDirectory, cfg.InstanceArchive);
            if (!File.Exists(archive)) return;
            var root = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData), "PrismLauncher", "instances", cfg.PrismInstance);
            if (!Directory.Exists(root))
            {
                Directory.CreateDirectory(root);
                ZipFile.ExtractToDirectory(archive, root, true);
            }
        }
        catch (Exception ex)
        {
            StatusText.Text = "Instance : " + ex.Message;
        }
    }

    async void Play_Click(object s, RoutedEventArgs e)
    {
        if (launching) return;
        launching = true;
        PlayButton.IsEnabled = false;

        prismPath = FindPrism();
        if (prismPath == null)
        {
            StatusText.Text = "⚠ Prism Launcher n'est pas installé";
            MessageBox.Show(
                "Installe Prism Launcher une fois, puis relance Valhalla.",
                "Valhalla",
                MessageBoxButton.OK,
                MessageBoxImage.Warning);
            PlayButton.IsEnabled = true;
            launching = false;
            return;
        }

        InstallInstanceSilently();
        StatusText.Text = "Lancement de Minecraft…";
        await Task.Delay(150);

        var direct = DirectConnectCheck.IsChecked == true ? $" --server \"{cfg.Server}\"" : "";
        try
        {
            Process.Start(new ProcessStartInfo(prismPath, $"--launch \"{cfg.PrismInstance}\"{direct}")
            {
                UseShellExecute = false,
                CreateNoWindow = true,
                WindowStyle = ProcessWindowStyle.Hidden
            });
            StatusText.Text = "✓ Minecraft lancé";
        }
        catch (Exception ex)
        {
            StatusText.Text = "Erreur : " + ex.Message;
        }

        await Task.Delay(500);
        PlayButton.IsEnabled = true;
        launching = false;
    }

    void RamSlider_ValueChanged(object s, RoutedPropertyChangedEventArgs<double> e)
    {
        if (RamValueText != null)
            RamValueText.Text = $"{(int)e.NewValue} Go";
        if (uiReady) SaveSettings();
    }

    void DirectConnect_Changed(object s, RoutedEventArgs e)
    {
        if (uiReady) SaveSettings();
    }

    async void CheckUpdate_Click(object s, RoutedEventArgs e)
    {
        await LoadRemoteConfig();
        await CheckLauncherUpdate(true);
    }

    async Task LoadRemoteConfig()
    {
        if (string.IsNullOrWhiteSpace(cfg.UpdateManifestUrl)) return;
        try
        {
            var json = await http.GetStringAsync(cfg.UpdateManifestUrl);
            var m = JsonSerializer.Deserialize<UpdateManifest>(json, new JsonSerializerOptions { PropertyNameCaseInsensitive = true });
            if (m == null) return;
            if (m.Server != null && !string.IsNullOrWhiteSpace(m.Server.Address))
                cfg.Server = $"{m.Server.Address}:{m.Server.Port}";
            if (m.Minecraft != null && !string.IsNullOrWhiteSpace(m.Minecraft.Version))
                cfg.MinecraftVersion = m.Minecraft.Version;
            if (m.Modpack != null)
            {
                if (!string.IsNullOrWhiteSpace(m.Modpack.Name)) cfg.ModpackName = m.Modpack.Name;
                if (!string.IsNullOrWhiteSpace(m.Modpack.Version)) cfg.PackVersion = m.Modpack.Version;
                if (!string.IsNullOrWhiteSpace(m.Modpack.Type)) cfg.Loader = m.Modpack.Type;
            }
            Refresh();
        }
        catch { }
    }

    async Task CheckLauncherUpdate(bool manual)
    {
        if (string.IsNullOrWhiteSpace(cfg.UpdateManifestUrl))
        {
            if (manual) MessageBox.Show("Le serveur de mises à jour n'est pas configuré.", "Valhalla Update");
            return;
        }

        try
        {
            var json = await http.GetStringAsync(cfg.UpdateManifestUrl);
            var m = JsonSerializer.Deserialize<UpdateManifest>(json, new JsonSerializerOptions { PropertyNameCaseInsensitive = true });
            if (m == null || !Version.TryParse(m.LauncherVersion, out var remote)) return;

            var current = typeof(MainWindow).Assembly.GetName().Version ?? new Version(0, 0);
            if (remote <= current)
            {
                UpdateText.Text = "Valhalla est à jour";
                if (manual) MessageBox.Show("Valhalla est à jour.");
                return;
            }

            UpdateText.Text = $"Mise à jour {m.LauncherVersion} disponible";
            if (string.IsNullOrWhiteSpace(m.ReleaseUrl))
            {
                MessageBox.Show("La mise à jour est annoncée mais aucun installateur n'est publié.");
                return;
            }

            if (MessageBox.Show(
                $"Valhalla {m.LauncherVersion} est disponible. Installer maintenant ?",
                "Mise à jour",
                MessageBoxButton.YesNo) != MessageBoxResult.Yes)
                return;

            var updateDir = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData), "Valhalla", "updates", m.LauncherVersion);
            Directory.CreateDirectory(updateDir);

            var partial = Path.Combine(updateDir, "Valhalla-Setup.exe.download");
            var setup = Path.Combine(updateDir, "Valhalla-Setup.exe");
            if (File.Exists(partial)) File.Delete(partial);
            if (File.Exists(setup)) File.Delete(setup);

            using (var response = await http.GetAsync(m.ReleaseUrl, HttpCompletionOption.ResponseHeadersRead))
            {
                response.EnsureSuccessStatusCode();
                await using var input = await response.Content.ReadAsStreamAsync();
                await using var output = new FileStream(partial, FileMode.CreateNew, FileAccess.Write, FileShare.None, 81920, true);
                await input.CopyToAsync(output);
                await output.FlushAsync();
            }

            var info = new FileInfo(partial);
            if (info.Length < 1_000_000)
                throw new InvalidDataException($"Téléchargement incomplet ({info.Length} octets).");

            if (!string.IsNullOrWhiteSpace(m.Sha256))
            {
                await using var check = File.OpenRead(partial);
                var actual = Convert.ToHexString(await SHA256.HashDataAsync(check)).ToLowerInvariant();
                var expected = m.Sha256.Replace("sha256:", "", StringComparison.OrdinalIgnoreCase).Trim().ToLowerInvariant();
                if (!string.Equals(actual, expected, StringComparison.OrdinalIgnoreCase))
                    throw new InvalidDataException("Le contrôle SHA-256 de la mise à jour a échoué.");
            }

            File.Move(partial, setup, true);

            var psi = new ProcessStartInfo(setup, "/VERYSILENT /CLOSEAPPLICATIONS /RESTARTAPPLICATIONS /SUPPRESSMSGBOXES")
            {
                UseShellExecute = true,
                WorkingDirectory = updateDir
            };

            if (Process.Start(psi) == null)
                throw new InvalidOperationException("Impossible de lancer l'installateur de mise à jour.");

            Application.Current.Shutdown();
        }
        catch (Exception ex)
        {
            MessageBox.Show("Mise à jour impossible : " + ex.Message, "Valhalla Update");
        }
    }
}

public class LauncherConfig
{
    public string ModpackName { get; set; } = "VANILLA";
    public string MinecraftVersion { get; set; } = "26.3";
    public string Loader { get; set; } = "Vanilla";
    public string PackVersion { get; set; } = "1.0.0";
    public string Server { get; set; } = "109.239.152.82:26065";
    public string PrismInstance { get; set; } = "Valhalla-Vanilla-26.3";
    public string InstanceArchive { get; set; } = "Valhalla-Vanilla-26.3.zip";
    public string UpdateManifestUrl { get; set; } = "";
}

public class UserSettings
{
    public int RamMb { get; set; } = 8192;
    public bool DirectConnect { get; set; } = true;
}

public class UpdateManifest
{
    public string LauncherVersion { get; set; } = "0.0.0";
    public string ReleaseUrl { get; set; } = "";
    public string Sha256 { get; set; } = "";
    public RemoteServer? Server { get; set; }
    public RemoteMinecraft? Minecraft { get; set; }
    public RemoteModpack? Modpack { get; set; }
}

public class RemoteServer
{
    public string Address { get; set; } = "";
    public int Port { get; set; } = 25565;
}

public class RemoteMinecraft
{
    public string Version { get; set; } = "";
}

public class RemoteModpack
{
    public string Type { get; set; } = "";
    public string Name { get; set; } = "";
    public string Version { get; set; } = "";
    public string Url { get; set; } = "";
}
