module.exports = {
  apps: [
    {
      name: "sl-backend",
      script: "dist/server.js",
      cwd: "/var/www/solvelitigation/backend",
      env: {
        NODE_ENV: "production",
        PORT: 4000,
        AUTH_COOKIE_NAME: "sl_auth",
        NLP_BASE_URL: "http://127.0.0.1:8000",
        JWT_SECRET: "90664e3508dbf4862cee37fa12f446a816a91332bf76a5a590a0c729b7583152fd829c73ecf3ecc1a4e4f1c8970d1feba77a81cba75879f15d7d82d5",
        SYSTEM_INGEST_USER_ID: "69841d4f065476f7a38de668",
        MONGODB_URI: "mongodb://sl_admin:solvelitigation%401966@127.0.0.1:27017/solvelitigation?authSource=admin"
      }
    }
  ]
}
