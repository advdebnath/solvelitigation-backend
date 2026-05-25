import { Request, Response, NextFunction } from "express";


// ======================================================
// 🔥 COURT-AWARE RBAC MIDDLEWARE
// ======================================================

export const requireCourtAccess = (
    allowedCourtScopes: string[]
) => {

    return async (
        req: any,
        res: Response,
        next: NextFunction
    ) => {

        try {

            const user = req.user;

            if (!user) {

                return res.status(401).json({
                    success: false,
                    message: "Unauthorized"
                });
            }

            // ==================================================
            // 🔥 SUPERADMIN BYPASS
            // ==================================================

            if (
                user.role === "superadmin"
            ) {
                return next();
            }

            const userCourtScopes = Array.isArray(
                user.courtScope
            )
                ? user.courtScope
                : [];

            const hasCourtAccess =
                allowedCourtScopes.some(
                    (scope) =>
                        userCourtScopes.includes(scope)
                );

            if (!hasCourtAccess) {

                return res.status(403).json({
                    success: false,
                    message:
                        "Court scope access denied"
                });
            }

            next();

        } catch (error: any) {

            console.error(
                "❌ COURT RBAC ERROR:",
                error
            );

            return res.status(500).json({
                success: false,
                message:
                    "Court RBAC middleware failed"
            });
        }
    };
};
