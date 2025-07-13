from . import commands, menu

def register_handlers(dp):
    dp.include_router(commands.router)
    dp.include_router(menu.router)