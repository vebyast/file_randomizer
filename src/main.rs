#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")] // hide console window on Windows in release

use eframe::egui;
use rand::seq::IteratorRandom;
use serde::{Deserialize, Serialize};
use std::path::PathBuf;

const CONFIG_APP_NAME: &str = "file-randomizer";

fn main() -> eframe::Result {
    env_logger::init(); // Log to stderr (if you run with `RUST_LOG=debug`).

    let init_conf = FileRandomizer::load();

    eframe::run_native(
        "File Randomizer",
        eframe::NativeOptions {
            viewport: egui::ViewportBuilder::default().with_inner_size([480.0, 120.0]),
            ..Default::default()
        },
        Box::new(|_cc| Ok(Box::new(init_conf))),
    )
}

#[derive(Serialize, Deserialize)]
struct FileRandomizer {
    dir: Option<PathBuf>,
    file: Option<PathBuf>,
}

impl Default for FileRandomizer {
    fn default() -> Self {
        Self {
            dir: Default::default(),
            file: Default::default(),
        }
    }
}

impl FileRandomizer {
    fn load() -> Self {
        confy::load(CONFIG_APP_NAME, None)
            .expect("fatal error while attempting to create or load configuration")
    }

    fn store(&self) {
        confy::store(CONFIG_APP_NAME, None, self)
            .expect("fatal error while attempting to create or load configuration")
    }
}

impl eframe::App for FileRandomizer {
    fn update(&mut self, ctx: &egui::Context, _frame: &mut eframe::Frame) {
        let mut rng = rand::rng();

        egui::CentralPanel::default().show(ctx, |ui| {
            ui.heading("File Randomizer");
            ui.horizontal(|ui| {
                if ui.button("Select directory").clicked() {
                    self.dir = rfd::FileDialog::new().pick_folder();
                    self.store();
                }

                match &self.dir {
                    Some(d) => ui.label(d.display().to_string()),
                    None => ui.label("No directory selected"),
                };
            });
            ui.horizontal(|ui| {
                if ui.button("Randomize file").clicked() {
                    if let Some(d) = &self.dir {
                        self.file = std::fs::read_dir(d)
                            .expect("Failure while listing directory")
                            .filter_map(|el| el.ok())
                            .filter(|de| !de.path().is_dir())
                            .choose(&mut rng)
                            .map(|de| de.path());
                        self.store();
                    };
                }
                match &self.file {
                    Some(f) => ui.label(f.display().to_string()),
                    None => ui.label("No file selected"),
                };
            });
            ui.horizontal(|ui| {
                if ui.button("Open directory").clicked() {
                    if let Some(d) = &self.dir {
                        showfile::show_path_in_file_manager(d);
                    }
                }

                if ui.button("Open file").clicked() {
                    if let Some(f) = &self.file {
                        let _ = open::that(f);
                    }
                }
            });
        });
    }
}
