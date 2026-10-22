use loco_rs::cli;
use rust_loco_sqlite_starter::app::App;

#[tokio::main]
async fn main() -> eyre::Result<()> {
    cli::main::<App>().await
}
