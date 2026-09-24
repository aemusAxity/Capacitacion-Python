import httpx2
import typer
from pydantic_settings import BaseSettings


# 1. Configuración
# Leer las variables del archivo .env y pydantic valida la URL
class Settings(BaseSettings):
    api_url: str
    api_key: str

    class Config:
        env_file = ".env"


config = Settings()

# 2. Inicializar Typer
app = typer.Typer(
    name="orders-cli",
    help="Herramienta para la gestion de ordenes.",
    add_completion=False,  # Apagar autocompletado para evitar config complejas
)


# 3. Primer comando: Listar (Usa peticiones HTTP reales a una API pública de prueba)
@app.command()
# Obtiene una lista de las órdenes recientes
def listar(
    limite: int = typer.Option(5, help="Número máximo de órdenes a listar")
) -> None:

    if limite < 1 or limite > 5:
        typer.secho(
            "Valor inválido, asegurate de poner un valor entre el 1 y el 5",
            fg=typer.colors.YELLOW,
            bold=True,
        )
        raise typer.Exit(code=1)  # Mata el programa de forma limpia

    typer.echo(f"Conectando a {config.api_url} (Autenticado)...")

    try:
        # Usamos una API pública real para el ejemplo
        # (devuelve posts que fingirán ser órdenes)
        respuesta = httpx2.get(f"{config.api_url}/posts")
        respuesta.raise_for_status()  # Lanza error si no es 200 OK
        ordenes = respuesta.json()

        typer.secho("\nLista de Órdenes:", fg=typer.colors.CYAN, bold=True)
        for orden in ordenes[:limite]:
            typer.echo(f"  [ID: {orden['id']}] - Título: {orden['title'][:30]}...")

    except httpx2.HTTPError as e:
        typer.secho(f"Error de conexion a la API: {e}", fg=typer.colors.RED)


# 4. Segundo comando: Crear ordenes
@app.command()
# Crea una orden nueva para un cliente.
def crear(
    cliente: str = typer.Argument(..., help="Nombre del cliente"),
    total: float = typer.Argument(..., help="Total de la compra en formato decimal"),
) -> None:
    # Aquí iría el httpx.post(), pero lo simularemos con la interfaz para el laboratorio
    typer.secho(
        f"\nOrden creada exitosamente en la API para el cliente: {cliente.upper()}",
        fg=typer.colors.GREEN,
    )
    typer.echo(f"Total facturado: ${total:.2f}")


# 5. Tercer comando: Borrar una orden por su ID (Con advertencia de seguridad)
@app.command()
def borrar(
    id_orden: int = typer.Argument(..., help="ID de la orden a eliminar"),
    forzar: bool = typer.Option(
        False, "--forzar", "-f", help="Borrar sin pedir confirmación"
    ),
) -> None:

    # 1. Pedimos confirmación si no usaron la bandera --forzar
    if not forzar:
        typer.secho(
            f"ESTÁS A PUNTO DE BORRAR LA ORDEN {id_orden}",
            fg=typer.colors.YELLOW,
            bold=True,
        )
        confirmacion = typer.confirm("¿Continuar?")
        if not confirmacion:
            typer.echo("Operacion cancelada")
            raise typer.Exit()

    # 2. Simulamos la petición de borrado
    typer.echo(f"Conectando a la API para borrar orden {id_orden}...")

    try:
        # Simulamos que la API devuelve un 200 OK al borrar
        # httpx.delete(f"{config.api_url}/posts/{id_orden}")

        typer.secho(
            f"La orden {id_orden} ha sido eliminada", fg=typer.colors.GREEN, bold=True
        )

    except Exception as e:
        typer.secho(f"Error al intentar borrar la orden: {e}", fg=typer.colors.RED)


if __name__ == "__main__":
    app()
