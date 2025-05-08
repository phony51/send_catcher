import click

from _cli import catcher, proxy, init, auth


cli = click.Group()
cli.add_command(proxy.proxy_group)
cli.add_command(catcher.catcher_group)
cli.add_command(init.init)
cli.add_command(auth.auth)

if __name__ == "__main__":
    cli()