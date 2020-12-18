"""Horseman sample
"""

def start(config):
    import bjoern
    from sample.app import app

    app.config.update(config.app)

    print('Running.')
    bjoern.run(
        app, config.server.host,
        int(config.server.port), reuse_port=True)


if __name__ == "__main__":
    from omegaconf import OmegaConf

    baseconf = OmegaConf.load('config.yaml')
    override = OmegaConf.from_cli()
    config = OmegaConf.merge(baseconf, override)
    start(config)
