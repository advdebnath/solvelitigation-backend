"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
// FILE: src/config/db.ts
const gridfs_1 = require("../utils/gridfs");
const mongoose_1 = __importDefault(require("mongoose"));
const bcryptjs_1 = __importDefault(require("bcryptjs"));
const user_model_1 = require("../models/user.model");
const MONGO_URI = process.env.MONGODB_URI || 'mongodb://localhost:27017/solvelitigation';
const SALT_ROUNDS = Number.isFinite(Number(process.env.BCRYPT_SALT_ROUNDS))
    ? Math.max(4, Math.min(15, Number(process.env.BCRYPT_SALT_ROUNDS)))
    : 10;
/**
 * Establish a MongoDB connection (idempotent).
 * - Logs status safely (guards against `connection.connection.db` undefined).
 * - Ensures a superadmin user exists (race-safe upsert).
 */
const connectDB = async () => {
    try {
        if (!process.env.MONGODB_URI) {
            console.warn('[WARNING]  MONGODB_URI is not defined in .env. Using fallback.');
        }
        const conn = await mongoose_1.default.connect(MONGO_URI, {
            maxPoolSize: 10,
            serverSelectionTimeoutMS: 5000,
            socketTimeoutMS: 45000,
        });
        await (0, gridfs_1.initGridFS)(); // ✅ initialize GridFS after connection
        const dbName = conn.connection?.db?.databaseName;
        console.log('[OK] MongoDB connected:', MONGO_URI);
        console.log('📋 Database:', dbName ?? '<unknown>');
        // Helpful: confirm models are compiled (avoids first-use latency surprises)
        // Object.values(mongoose.models).forEach((m) => void m); // no-op touch
        // Quick telemetry
        const userCount = await user_model_1.User.estimatedDocumentCount().catch(async () => user_model_1.User.countDocuments());
        console.log(`[STATS] Total users: ${userCount}`);
        // ---- Ensure a superadmin exists (race-safe) ----
        // Use upsert to avoid races; setOnInsert only runs when creating.
        const defaultPassword = process.env.SUPERADMIN_PASSWORD || 'superadmin123';
        const hashed = await bcryptjs_1.default.hash(defaultPassword, SALT_ROUNDS);
        const upsertDoc = await user_model_1.User.findOneAndUpdate({ role: 'superadmin' }, // match any existing superadmin
        {
            $setOnInsert: {
                name: 'Super Admin',
                email: 'superadmin@solvelitigation.com',
                password: hashed,
                role: 'superadmin',
                isVerified: true,
            },
        }, { new: true, upsert: true, setDefaultsOnInsert: true }).lean();
        if (upsertDoc?.email === 'superadmin@solvelitigation.com') {
            // We don't actually know if it was created vs already present from `.lean()`.
            // Peek once more to decide what to log:
            const createdNow = await user_model_1.User.countDocuments({
                email: 'superadmin@solvelitigation.com',
                createdAt: { $gte: new Date(Date.now() - 60000) }, // within last minute
            }).catch(() => 0);
            if (createdNow > 0 && userCount === 0) {
                console.log('🛡️  Superadmin created: superadmin@solvelitigation.com');
            }
            else {
            }
        }
        else {
        }
        return { uri: MONGO_URI, dbName };
    }
    catch (error) {
        const msg = error?.message || String(error);
        console.error('[ERROR] MongoDB connection failed:', msg);
        if (/ECONNREFUSED/i.test(msg)) {
            console.error('[SOCKET] MongoDB server is not running.');
        }
        else if (/auth/i.test(msg)) {
            console.error('🔐 Authentication failed.');
        }
        else if (/timeout/i.test(msg)) {
            console.error('[TIME] Connection timeout.');
        }
        if (process.env.NODE_ENV === 'production') {
            process.exit(1);
        }
    }
};
/* ----------------------------- Connection Events ---------------------------- */
mongoose_1.default.connection.on('connected', () => {
    console.log('🔗 Mongoose connected');
});
mongoose_1.default.connection.on('error', (err) => {
});
mongoose_1.default.connection.on('disconnected', () => {
    console.log('[SOCKET] Mongoose disconnected');
});
/* ------------------------------ Graceful exit ------------------------------- */
const shutdown = async (signal) => {
    try {
        console.log(`🛑 Received ${signal}. Closing MongoDB connection...`);
        await mongoose_1.default.connection.close();
        console.log('[OK] MongoDB connection closed. Bye!');
    }
    catch (e) {
        console.error('[ERROR] Error during MongoDB shutdown:', e);
    }
    finally {
        process.exit(0);
    }
};
process.once('SIGINT', () => shutdown('SIGINT'));
process.once('SIGTERM', () => shutdown('SIGTERM'));
exports.default = connectDB;
