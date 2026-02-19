import "express";

declare global {
  namespace Express {
    interface User {
      _id: string;
      id?: string;
      name?: string;
      email?: string;
      role: "user" | "admin" | "superadmin";

      isVerified?: boolean;

      plan?: string;
      planStatus?: "active" | "inactive" | "expired" | "grace";
      planExpiresAt?: Date | null;

      usage?: {
        downloads: number;
        aiRequests: number;
        judgmentsViewed: number;
        lastViewedAt?: Date;
      };

      grace?: {
        downloads: number;
        aiRequests: number;
        judgmentsViewed: number;
      };
    }

    interface Request {
      user?: User;
      currentUser?: User;
    }

    namespace Multer {
      interface File {
        webkitRelativePath?: string;

        originalname: string;
        filename: string;
        path: string;
        size: number;
        mimetype: string;
      }
    }
  }
}

export {};
