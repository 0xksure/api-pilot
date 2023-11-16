use std::{
    fs,
    rc::{Rc},
    sync::{mpsc, Arc},
    thread, time,
};

use crate::{
    openai::{gen_openaifunctions_from_swagger, OpenAIFunctionsTrait},
    swagger::Swagger,
};
use clap::{Parser, Subcommand};

pub mod openai;
pub mod swagger;
extern crate oas3;

#[derive(Debug, Parser)]
#[command(name = "OpenAiSwagger")]
#[command(about="Converts a swagger file to openai functions",long_about=None)]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Debug, Subcommand)]
enum Commands {
    // generates a openAI function from a swagger 2 file
    #[command(arg_required_else_help = true)]
    Convert {
        swagger_file_path: String,
        output_file_path: String,
    },
    #[command(arg_required_else_help = true)]
    Listen {
        folder_path: String,
        output_file_path: String,
    },
}

fn main() {
    env_logger::init();
    let args = Cli::parse();
    match args.command {
        Commands::Convert {
            swagger_file_path,
            output_file_path,
        } => {
            log::info!(
                "Generating openai functions from swagger file: {:?}",
                swagger_file_path
            );
            log::info!("Output file: {:?}", output_file_path);
            // load the swagger yaml
            let swagger = Swagger::from_file(&swagger_file_path).unwrap();
            println!("Swagger: {:?}", swagger);

            // convert to openAI
            let openai_funcs = gen_openaifunctions_from_swagger(swagger).unwrap();
            openai_funcs.write_to_json_file(&output_file_path).unwrap();
        }
        Commands::Listen {
            folder_path,
            output_file_path,
        } => {
            let (tx, rx) = mpsc::channel();
            let output_file = format!("{}/openai.json", output_file_path);
            let folder_path_rc = Arc::new(folder_path);
            let mut swagger_hash = String::from("");
            thread::spawn(move || loop {
                let fp = fs::read_dir(folder_path_rc.clone().as_ref()).unwrap();
                fp.for_each(|f| {
                    let file_rc = Rc::new(f.unwrap());
                    if file_rc
                        .file_name()
                        .to_str()
                        .unwrap()
                        .contains("swagger.json")
                    {
                        let file_bytes = fs::read(file_rc.path()).unwrap();
                        let new_swagger_hash = sha256::digest(&file_bytes).to_string();
                        if new_swagger_hash != swagger_hash {
                            println!("👀 Swagger file changed");
                            swagger_hash = new_swagger_hash;
                            tx.send(file_bytes).unwrap();
                        }
                    }
                });
                thread::sleep(time::Duration::from_secs(1));
            });

            for file_bytes in rx {
                let swagger = Swagger::from_json(&String::from_utf8(file_bytes).unwrap()).unwrap();
                let openai_funcs = gen_openaifunctions_from_swagger(swagger).unwrap();

                match openai_funcs.write_to_json_file(&output_file) {
                    Ok(_) => println!("📜 Wrote openai functions to file.\n"),
                    Err(e) => println!("❌ Error writing openai functions to file: {:?}\n", e),
                }
            }
        }
    }
}
