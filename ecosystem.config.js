module.exports = {
  apps: [
    {
      name: "solvelitigation-backend",
      script: "dist/server.js",
      cwd: "/var/www/solvelitigation/backend",
      instances: 1,
      exec_mode: "fork",
      env: {
        NODE_ENV: "production",
        PORT: 4000,
        AUTH_COOKIE_NAME: "sl_auth",
        JWT_SECRET: "90664e3508dbf4862cee37fa12f446a816a91332bf76a5a590a0c729b7583152",
        MONGO_URI: "mongodb://sl_admin:solvelitigation%401966@127.0.0.1:27017/solvelitigation?authSource=admin"
      }
    }
  ]
};
