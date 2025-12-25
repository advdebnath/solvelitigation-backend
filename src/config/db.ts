// FILE: src/config/db.ts
import { initGridFS } from "@/utils/gridfs";
import mongoose from 'mongoose';
import bcrypt from 'bcryptjs';
import { User } from '@/models/user.model';


const MONGO_URI = process.env.MONGODB_URI || 'mongodb://localhost:27017/solvelitigation';
const SALT_ROUNDS = Number.isFinite(Number(process.env.BCRYPT_SALT_ROUNDS))
  ? Math.max(4, Math.min(15, Number(process.env.BCRYPT_SALT_ROUNDS)))
  : 10;

type ConnectResult = {
  uri: string;
  dbName: string | undefined;
};

/**
 * Establish a MongoDB connection (idempotent).
 * - Logs status safely (guards against `connection.connection.db` undefined).
 * - Ensures a superadmin user exists (race-safe upsert).
 */
const connectDB = async (): Promise<ConnectResult | void> => {
  try {
    if (!process.env.MONGODB_URI) {
      console.warn('[WARNING]  MONGODB_URI is not defined in .env. Using fallback.');
    }

      const conn = await mongoose.connect(MONGO_URI, {
        maxPoolSize: 10,
        serverSelectionTimeoutMS: 5000,
        socketTimeoutMS: 45000,
      });

      await initGridFS();  // ✅ initialize GridFS after connection


    const dbName = conn.connection?.db?.databaseName;
    console.log('[OK] MongoDB connected:', MONGO_URI);
    console.log('📋 Database:', dbName ?? '<unknown>');

    // Helpful: confirm models are compiled (avoids first-use latency surprises)
    // Object.values(mongoose.models).forEach((m) => void m); // no-op touch

    // Quick telemetry
    const userCount = await User.estimatedDocumentCount().catch(async () => User.countDocuments());
    console.log(`[STATS] Total users: ${userCount}`);

    // ---- Ensure a superadmin exists (race-safe) ----
    // Use upsert to avoid races; setOnInsert only runs when creating.
    const defaultPassword = process.env.SUPERADMIN_PASSWORD || 'superadmin123';
    const hashed = await bcrypt.hash(defaultPassword, SALT_ROUNDS);

    const upsertDoc = await User.findOneAndUpdate(
      { role: 'superadmin' }, // match any existing superadmin
      {
        $setOnInsert: {
          name: 'Super Admin',
          email: 'superadmin@solvelitigation.com',
          password: hashed,
          role: 'superadmin',
          isVerified: true,
        },
      },
      { new: true, upsert: true, setDefaultsOnInsert: true }
    ).lean();

    if ((upsertDoc as any)?.email === 'superadmin@solvelitigation.com') {
      // We don't actually know if it was created vs already present from `.lean()`.
      // Peek once more to decide what to log:
      const createdNow = await User.countDocuments({
        email: 'superadmin@solvelitigation.com',
        createdAt: { $gte: new Date(Date.now() - 60_000) }, // within last minute
      }).catch(() => 0);

      if (createdNow > 0 && userCount === 0) {
        console.log('🛡️  Superadmin created: superadmin@solvelitigation.com');
      } else {
      }
    } else {
    }

    return { uri: MONGO_URI, dbName };
  } catch (error: any) {
    const msg = error?.message || String(error);
    console.error('[ERROR] MongoDB connection failed:', msg);

    if (/ECONNREFUSED/i.test(msg)) {
      console.error('[SOCKET] MongoDB server is not running.');
    } else if (/auth/i.test(msg)) {
      console.error('🔐 Authentication failed.');
    } else if (/timeout/i.test(msg)) {
      console.error('[TIME] Connection timeout.');
    }

    if (process.env.NODE_ENV === 'production') {
      process.exit(1);
    }
  }
};

/* ----------------------------- Connection Events ---------------------------- */

mongoose.connection.on('connected', () => {
  console.log('🔗 Mongoose connected');
});

mongoose.connection.on('error', (err) => {
});

mongoose.connection.on('disconnected', () => {
  console.log('[SOCKET] Mongoose disconnected');
});

/* ------------------------------ Graceful exit ------------------------------- */

const shutdown = async (signal: string) => {
  try {
    console.log(`🛑 Received ${signal}. Closing MongoDB connection...`);
    await mongoose.connection.close();
    console.log('[OK] MongoDB connection closed. Bye!');
  } catch (e) {
    console.error('[ERROR] Error during MongoDB shutdown:', e);
  } finally {
    process.exit(0);
  }
};

process.once('SIGINT', () => shutdown('SIGINT'));
process.once('SIGTERM', () => shutdown('SIGTERM'));

export default connectDB;
export type { ConnectResult };




