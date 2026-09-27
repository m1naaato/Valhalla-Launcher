using CmlLib.Core;
using CmlLib.Core.Auth;
using CmlLib.Core.Auth.Microsoft;
using CmlLib.Core.Installer.Forge;
using CmlLib.Core.ProcessBuilder;
using System;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Sockets;
using System.Text;
using System.Security.Cryptography;
using System.Text.Json;
using System.Threading.Tasks;
using System.Windows;

namespace ValhallaLauncher;

public partial class MainWindow : Window
{
    readonly HttpClient http = new();
    LauncherConfig cfg = new();
    bool launching;
    bool uiReady;
    MSession? minecraftSession;
    readonly JELoginHandler loginHandler = JELoginHandlerBuilder.BuildDefault();
    string? forgeVersion;
    string UserCfg => Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData), "Valhalla", "settings.json");
    string GameRoot => Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData), "Valhalla", "DDSS");
    MinecraftLauncher CreateGameLauncher() => new(new MinecraftPath(GameRoot));

    public MainWindow()
    {
        InitializeComponent();
        uiReady = true;
        LoadConfig();
        LoadSettings();
        Refresh();
        Loaded += async (_, _) =>
        {
            await RestoreMinecraftSession();
            await LoadRemoteConfig();
            await RefreshServerStatus();
            await CheckServerPack(false);
            await CheckLauncherUpdate(false);
        };
    }

    async Task RestoreMinecraftSession()
    {
        try
        {
            minecraftSession = await loginHandler.AuthenticateSilently();
            ShowMinecraftAccountConnected();
        }
        catch { }
    }

    void ShowMinecraftAccountConnected()
    {
        if (minecraftSession == null) return;
        AccountStateText.Text = minecraftSession.Username;
        AccountActionButton.Content = "MINECRAFT CONNECTÉ";
        AccountActionButton.IsEnabled = false;
        DisconnectButton.IsEnabled = true;
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

    async void Compte_Click(object s, RoutedEventArgs e)
    {
        AccountActionButton.IsEnabled = false;
        try
        {
            minecraftSession = await loginHandler.AuthenticateInteractively();
            ShowMinecraftAccountConnected();
            StatusText.Text = "✓ Compte Minecraft connecté";
        }
        catch (Exception ex)
        {
            AccountActionButton.IsEnabled = true;
            StatusText.Text = "Connexion Minecraft impossible";
            MessageBox.Show(ex.Message, "Valhalla - Minecraft", MessageBoxButton.OK, MessageBoxImage.Warning);
        }
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
            if (HomeRamSlider != null) HomeRamSlider.Value = RamSlider.Value;
            if (HomeRamValueText != null) HomeRamValueText.Text = $"{(int)RamSlider.Value} Go / 16 Go";
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
        if (ServerAddressText != null) ServerAddressText.Text = cfg.Server;
        PackNameText.Text = cfg.ModpackName;
        PackInfoText.Text = $"Minecraft {cfg.MinecraftVersion} • {cfg.Loader} • pack {cfg.PackVersion}";
        ServerStatusText.Text = string.IsNullOrWhiteSpace(cfg.Server) ? "NON CONFIGURÉ" : "Vérification...";
        ServerPlayersText.Text = "Joueurs : --/--";
        StatusText.Text = "Valhalla prêt à installer DD&SS";
    }

    async Task RefreshServerStatus()
    {
        if (string.IsNullOrWhiteSpace(cfg.Server)) return;
        try
        {
            var parts = cfg.Server.Split(':', 2);
            var host = parts[0];
            var port = parts.Length > 1 && int.TryParse(parts[1], out var p) ? p : 25565;
            using var tcp = new TcpClient();
            using var timeout = new CancellationTokenSource(TimeSpan.FromSeconds(4));
            await tcp.ConnectAsync(host, port, timeout.Token);
            using var stream = tcp.GetStream();

            static void WriteVarInt(Stream s, int value) { while (true) { if ((value & ~0x7F) == 0) { s.WriteByte((byte)value); return; } s.WriteByte((byte)((value & 0x7F) | 0x80)); value = (int)((uint)value >> 7); } }
            static int ReadVarInt(Stream s) { int n = 0, r = 0; byte b; do { if (n++ > 5) throw new InvalidDataException(); int v = s.ReadByte(); if (v < 0) throw new EndOfStreamException(); b = (byte)v; r |= (b & 0x7F) << (7 * (n - 1)); } while ((b & 0x80) != 0); return r; }

            using var packet = new MemoryStream();
            WriteVarInt(packet, 0); WriteVarInt(packet, -1);
            var hostBytes = Encoding.UTF8.GetBytes(host); WriteVarInt(packet, hostBytes.Length); packet.Write(hostBytes);
            packet.WriteByte((byte)(port >> 8)); packet.WriteByte((byte)port); WriteVarInt(packet, 1);
            WriteVarInt(stream, (int)packet.Length); packet.Position = 0; await packet.CopyToAsync(stream, timeout.Token);
            stream.WriteByte(1); stream.WriteByte(0);
            _ = ReadVarInt(stream); _ = ReadVarInt(stream); int len = ReadVarInt(stream);
            var data = new byte[len]; int read = 0; while (read < len) { int n = await stream.ReadAsync(data.AsMemory(read, len - read), timeout.Token); if (n == 0) throw new EndOfStreamException(); read += n; }
            using var doc = JsonDocument.Parse(data);
            var players = doc.RootElement.GetProperty("players");
            var online = players.GetProperty("online").GetInt32();
            var max = players.GetProperty("max").GetInt32();
            ServerStatusText.Text = "EN LIGNE";
            ServerPlayersText.Text = $"Joueurs : {online}/{max}";
            ServerDot.Fill = System.Windows.Media.Brushes.LimeGreen;
        }
        catch
        {
            ServerStatusText.Text = "HORS LIGNE";
            ServerPlayersText.Text = "Joueurs : --/--";
            ServerDot.Fill = System.Windows.Media.Brushes.IndianRed;
        }
    }

    async Task<MinecraftLauncher> PrepareGameAsync()
    {
        Directory.CreateDirectory(GameRoot);
        var launcher = CreateGameLauncher();
        var progress = new Progress<CmlLib.Core.Installers.InstallerProgressChangedEventArgs>(e =>
            StatusText.Text = $"Minecraft : {e.Name} ({e.ProgressedTasks}/{e.TotalTasks})");
        StatusText.Text = "Installation de Minecraft 1.12.2 et Java...";
        await launcher.InstallAsync("1.12.2");
        var vanilla = await launcher.GetVersionAsync("1.12.2");
        var javaPath = await launcher.GetJavaPath(vanilla);
        if (string.IsNullOrWhiteSpace(javaPath))
            throw new InvalidOperationException("Java 8 n'a pas pu être installé.");
        StatusText.Text = "Installation de Forge 1.12.2...";
        var forge = new ForgeInstaller(launcher);
        forgeVersion = await forge.Install("1.12.2", new ForgeInstallOptions
        {
            JavaPath = javaPath,
            FileProgress = progress
        });
        await launcher.InstallAsync(forgeVersion);
        return launcher;
    }

    async void Prepare_Click(object s, RoutedEventArgs e)
    {
        try
        {
            if (!await CheckServerPack(true)) return;
            await PrepareGameAsync();
            StatusText.Text = "✓ DD&SS, Forge et Minecraft sont prêts";
        }
        catch (Exception ex)
        {
            StatusText.Text = "Installation impossible";
            MessageBox.Show(ex.Message, "Valhalla - Installation", MessageBoxButton.OK, MessageBoxImage.Warning);
        }
    }

    async void Play_Click(object s, RoutedEventArgs e)
    {
        if (launching) return;
        launching = true;
        PlayButton.IsEnabled = false;
        try
        {
            minecraftSession = await loginHandler.Authenticate();
            ShowMinecraftAccountConnected();
            if (!await CheckServerPack(true)) return;
            var launcher = await PrepareGameAsync();
            var options = new MLaunchOption
            {
                Session = minecraftSession,
                MaximumRamMb = (int)RamSlider.Value * 1024
            };
            if (DirectConnectCheck.IsChecked == true)
            {
                var parts = cfg.Server.Split(':', 2);
                options.ServerIp = parts[0];
                options.ServerPort = parts.Length > 1 && int.TryParse(parts[1], out var p) ? p : 25565;
            }
            StatusText.Text = "Lancement de DD&SS...";
            var game = await launcher.BuildProcessAsync(forgeVersion!, options);
            game.Start();
            StatusText.Text = "✓ Minecraft lancé";
            await Task.Delay(350);
            Application.Current.Shutdown();
        }
        catch (Exception ex)
        {
            StatusText.Text = "Lancement impossible";
            MessageBox.Show(ex.Message, "Valhalla - DD&SS", MessageBoxButton.OK, MessageBoxImage.Warning);
        }
        finally
        {
            launching = false;
            PlayButton.IsEnabled = true;
        }
    }

    void HomeRamSlider_ValueChanged(object s, RoutedPropertyChangedEventArgs<double> e)
    {
        if (HomeRamValueText != null) HomeRamValueText.Text = $"{(int)e.NewValue} Go / 16 Go";
        if (!uiReady || RamSlider == null) return;
        RamSlider.Value = e.NewValue;
        SaveSettings();
    }

    void MinecraftVersion_Changed(object s, System.Windows.Controls.SelectionChangedEventArgs e)
    {
        if (!uiReady || MinecraftVersionCombo?.SelectedItem is not System.Windows.Controls.ComboBoxItem item) return;
        var version = item.Content?.ToString();
        if (string.IsNullOrWhiteSpace(version)) return;
        cfg.MinecraftVersion = version;
        Refresh();
    }

    async void Disconnect_Click(object s, RoutedEventArgs e)
    {
        try { await loginHandler.Signout(); } catch { }
        minecraftSession = null;
        AccountStateText.Text = "Minecraft non connecté";
        AccountActionButton.Content = "CONNEXION";
        AccountActionButton.IsEnabled = true;
        DisconnectButton.IsEnabled = false;
        StatusText.Text = "✓ Déconnecté de Minecraft";
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
            if (!cfg.Loader.Equals("Forge", StringComparison.OrdinalIgnoreCase) && m.Minecraft != null && !string.IsNullOrWhiteSpace(m.Minecraft.Version))
                cfg.MinecraftVersion = m.Minecraft.Version;
            if (m.Modpack != null && !cfg.Loader.Equals("Forge", StringComparison.OrdinalIgnoreCase))
            {
                if (!string.IsNullOrWhiteSpace(m.Modpack.Name)) cfg.ModpackName = m.Modpack.Name;
                if (!string.IsNullOrWhiteSpace(m.Modpack.Version)) cfg.PackVersion = m.Modpack.Version;
                if (!string.IsNullOrWhiteSpace(m.Modpack.Type)) cfg.Loader = m.Modpack.Type;
            }
            Refresh();
        }
        catch { }
    }



    async Task<bool> CheckServerPack(bool repair)
    {
        if (string.IsNullOrWhiteSpace(cfg.ModpackManifestUrl)) return true;
        try
        {
            PackSyncText.Text = "Vérification du pack serveur...";
            var json = await http.GetStringAsync(cfg.ModpackManifestUrl);
            var manifest = JsonSerializer.Deserialize<ServerPackManifest>(json, new JsonSerializerOptions { PropertyNameCaseInsensitive = true });
            if (manifest == null) throw new InvalidDataException("Manifest invalide.");
            if (manifest.MinecraftVersion != "1.12.2" || !manifest.Loader.Equals("Forge", StringComparison.OrdinalIgnoreCase))
                throw new InvalidDataException("Le pack publié ne correspond pas à DD&SS 1.12.2 Forge.");
            if (manifest.Files == null || manifest.Files.Count < 100)
                throw new InvalidDataException("Le pack DD&SS est incomplet.");
            var missing = new List<ServerPackFile>();
            foreach (var file in manifest.Files ?? new())
            {
                var relative = file.Path.Replace('/', Path.DirectorySeparatorChar).TrimStart(Path.DirectorySeparatorChar);
                var gameRoot = GameRoot;
                var local = Path.GetFullPath(Path.Combine(gameRoot, relative));
                var root = Path.GetFullPath(GameRoot) + Path.DirectorySeparatorChar;
                if (!local.StartsWith(root, StringComparison.OrdinalIgnoreCase)) throw new InvalidDataException("Chemin invalide.");
                if (!File.Exists(local) || !await FileMatches(local, file)) missing.Add(file);
            }
            if (missing.Count == 0)
            {
                PackSyncText.Text = "Pack serveur synchronisé";
                PackSyncText.Foreground = System.Windows.Media.Brushes.LightGreen;
                PlayButton.IsEnabled = true;
                return true;
            }
            PackSyncText.Text = $"{missing.Count} fichier(s) requis manquant(s)";
            PackSyncText.Foreground = System.Windows.Media.Brushes.Orange;
            PlayButton.IsEnabled = false;
            if (!repair) return false;
            Directory.CreateDirectory(GameRoot);
            int done = 0;
            foreach (var file in missing)
            {
                if (string.IsNullOrWhiteSpace(file.Url)) throw new InvalidDataException($"URL absente : {file.Path}");
                var relative = file.Path.Replace('/', Path.DirectorySeparatorChar).TrimStart(Path.DirectorySeparatorChar);
                var local = Path.GetFullPath(Path.Combine(GameRoot, relative));
                Directory.CreateDirectory(Path.GetDirectoryName(local)!);
                PackSyncText.Text = $"Téléchargement {++done}/{missing.Count} : {Path.GetFileName(file.Path)}";
                var bytes = await http.GetByteArrayAsync(file.Url);
                var temporary = local + ".valhalla-download";
                try
                {
                    await File.WriteAllBytesAsync(temporary, bytes);
                    if (!await FileMatches(temporary, file)) throw new InvalidDataException($"Fichier invalide : {file.Path}");
                    File.Move(temporary, local, true);
                }
                finally { if (File.Exists(temporary)) File.Delete(temporary); }
            }
            PackSyncText.Text = "Pack serveur installé et vérifié";
            PackSyncText.Foreground = System.Windows.Media.Brushes.LightGreen;
            PlayButton.IsEnabled = true;
            return true;
        }
        catch (Exception ex)
        {
            PackSyncText.Text = "Pack serveur non prêt";
            PackSyncText.Foreground = System.Windows.Media.Brushes.IndianRed;
            PlayButton.IsEnabled = false;
            if (repair) MessageBox.Show("Impossible de préparer le pack : " + ex.Message, "Valhalla - Modpack");
            return false;
        }
    }

    static async Task<bool> FileMatches(string path, ServerPackFile file)
    {
        if (file.Size > 0 && new FileInfo(path).Length != file.Size) return false;
        if (string.IsNullOrWhiteSpace(file.Sha256)) return true;
        await using var stream = File.OpenRead(path);
        var actual = Convert.ToHexString(await SHA256.HashDataAsync(stream)).ToLowerInvariant();
        var expected = file.Sha256.Replace("sha256:", "", StringComparison.OrdinalIgnoreCase).Trim().ToLowerInvariant();
        return actual == expected;
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
    public string ModpackManifestUrl { get; set; } = "";
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


public class ServerPackManifest
{
    public string Name { get; set; } = "Valhalla Server Pack";
    public string Version { get; set; } = "1.0.0";
    public string MinecraftVersion { get; set; } = "";
    public string Loader { get; set; } = "";
    public List<ServerPackFile> Files { get; set; } = new();
}
public class ServerPackFile
{
    public string Path { get; set; } = "";
    public string Url { get; set; } = "";
    public string Sha256 { get; set; } = "";
    public long Size { get; set; }
}
