using System;
using System.IO;
using System.Windows;
using System.Windows.Threading;
namespace ValhallaLauncher { public partial class App : Application { public App(){DispatcherUnhandledException += OnUnhandledException;} private void OnUnhandledException(object sender, DispatcherUnhandledExceptionEventArgs e){try{var log=Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),"Valhalla","crash.log");Directory.CreateDirectory(Path.GetDirectoryName(log)!);File.WriteAllText(log,$"{DateTime.Now:O}\n{e.Exception}");MessageBox.Show($"Valhalla a rencontré une erreur.\n\n{e.Exception.Message}\n\nRapport :\n{log}","Valhalla - Erreur",MessageBoxButton.OK,MessageBoxImage.Error);}catch{} e.Handled=true;Shutdown(-1);}}}