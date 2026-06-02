module.exports = {
  apps: [
    {
      name: "sl-celery-worker",

      cwd: "/var/www/solvelitigation/nlp_service",

      script: ".venv/bin/celery",

      args: "-A app.celery_app worker -Q celery --loglevel=info",

      interpreter: "none",

      exec_mode: "fork",

      autorestart: true,

      watch: false,

      max_memory_restart: "2G",

      restart_delay: 5000,

      max_restarts: 20,

      min_uptime: "10s",

      env: {
        PYTHONUNBUFFERED: "1"
      }
    }
  ]
}
