module.exports = {
  apps: [
    {
      name: "sl-nlp",
      script: "/var/www/solvelitigation/nlp_service/.venv/bin/python",
      args: "-m app.main",
      cwd: "/var/www/solvelitigation/nlp_service",
      autorestart: true,
      max_restarts: 10,
      restart_delay: 3000,
      env: {
        PYTHONUNBUFFERED: "1",
      },
    },
  ],
};
