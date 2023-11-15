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
    Generate {
        swagger_file_path: String,
        output_file_path: String,
    },
}

fn main() {
    env_logger::init();
    let args = Cli::parse();
    match args.command {
        Commands::Generate {
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
    }
}
