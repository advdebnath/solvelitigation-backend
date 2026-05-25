module.exports = {
  apps: [

    // =====================================================
    // 🔥 BACKEND API
    // =====================================================

    {
      name: "sl-backend",

      cwd: "/var/www/solvelitigation/backend",

      script: "dist/server.js",

      interpreter: "node",

      exec_mode: "fork",

      autorestart: true,

      watch: false,

      max_memory_restart: "1G",

      restart_delay: 5000,

      env: {
        NODE_ENV: "production",
        PORT: 4000
      },

      error_file:
        "/home/sladmin/.pm2/logs/sl-backend-error.log",

      out_file:
        "/home/sladmin/.pm2/logs/sl-backend-out.log",

      log_date_format:
        "YYYY-MM-DD HH:mm:ss"
    },

    // =====================================================
    // 🔥 NLP API (FASTAPI)
    // =====================================================

    {
      name: "sl-nlp-api",

      cwd: "/var/www/solvelitigation/nlp_service",

      script:
        "/var/www/solvelitigation/nlp_service/.venv/bin/uvicorn",

      args:
        "app.main:app --host 0.0.0.0 --port 8000",

      interpreter: "none",

      exec_mode: "fork",

      autorestart: true,

      watch: false,

      max_memory_restart: "2G",

      restart_delay: 5000,

      kill_timeout: 10000,

      env: {

        PYTHONPATH:
          "/var/www/solvelitigation/nlp_service",

        PYTHONUNBUFFERED: "1",

        NODE_ENV: "production"
      },

      error_file:
        "/home/sladmin/.pm2/logs/sl-nlp-api-error.log",

      out_file:
        "/home/sladmin/.pm2/logs/sl-nlp-api-out.log",

      log_date_format:
        "YYYY-MM-DD HH:mm:ss"
    },

    // =====================================================
    // 🔥 CELERY WORKER
    // =====================================================

    {
      name: "sl-celery-worker",

      cwd: "/var/www/solvelitigation/nlp_service",

      script:
        "/var/www/solvelitigation/nlp_service/.venv/bin/celery",

      args:
        "-A app.celery_app worker -Q nlp --loglevel=info --concurrency=4",

      interpreter: "none",

      exec_mode: "fork",

      autorestart: true,

      watch: false,

      max_memory_restart: "2G",

      restart_delay: 10000,

      kill_timeout: 20000,

      env: {

        PYTHONPATH:
          "/var/www/solvelitigation/nlp_service",

        PYTHONUNBUFFERED: "1"
      },

      error_file:
        "/home/sladmin/.pm2/logs/sl-celery-worker-error.log",

      out_file:
        "/home/sladmin/.pm2/logs/sl-celery-worker-out.log",

      log_date_format:
        "YYYY-MM-DD HH:mm:ss"
    },

    // =====================================================
    // 🔥 INGESTION WORKER
    // =====================================================

    {
      name: "sl-ingestion-worker",

      cwd: "/var/www/solvelitigation/backend",

      script:
        "dist/workers/ingestionProcessing.worker.js",

      interpreter: "node",

      exec_mode: "fork",

      autorestart: true,

      watch: false,

      max_memory_restart: "1G",

      restart_delay: 5000,

      env: {

        NODE_ENV: "production"
      },

      error_file:
         "/home/sladmin/.pm2/logs/sl-ingestion-worker-error.log",

      out_file:
        "/home/sladmin/.pm2/logs/sl-ingestion-worker-out.log",

      log_date_format:
        "YYYY-MM-DD HH:mm:ss"
    },



    // =====================================================
    // 🔥 NEXT.JS FRONTEND
    // =====================================================

    {
      name: "sl-frontend",

      cwd: "/var/www/solvelitigation/frontend",

      script:
        ".next/standalone/server.js",

      interpreter: "node",

      exec_mode: "fork",

      autorestart: true,

      watch: false,

      max_memory_restart: "1G",

      restart_delay: 5000,

      env: {

        NODE_ENV: "production",

        PORT: 3000
      },

      error_file:
        "/home/sladmin/.pm2/logs/sl-frontend-error.log",

      out_file:
        "/home/sladmin/.pm2/logs/sl-frontend-out.log",

      log_date_format:
        "YYYY-MM-DD HH:mm:ss"
    }

  ]
};
