from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class AuthorizationDecision:
    subject: str
    action: str
    object: str
    object_owner: int | None
    required_permission: str
    policy: str
    decision: str
    reason: str

    def to_dict(self) -> dict:
        return asdict(self)


def authorize_invoice(user_id: int, role: str, invoice_id: int, owner_id: int | None) -> AuthorizationDecision:
    allowed = owner_id is not None and (role == "admin" or owner_id == user_id)
    if owner_id is None:
        reason = "Invoice không tồn tại."
    elif role == "admin":
        reason = "Admin được phép đọc invoice theo chính sách lab."
    elif owner_id == user_id:
        reason = "Người dùng hiện tại sở hữu invoice."
    else:
        reason = "Người dùng hiện tại không sở hữu invoice."
    return AuthorizationDecision(
        subject=f"user_id {user_id}", action="read invoice", object=f"invoice {invoice_id}",
        object_owner=owner_id, required_permission="owner or admin", policy="owner or admin",
        decision="allow" if allowed else "deny", reason=reason,
    )


def authorize_profile_fields(user_id: int, submitted_fields: set[str]) -> AuthorizationDecision:
    rejected = sorted(submitted_fields - {"email"})
    return AuthorizationDecision(
        subject=f"user_id {user_id}", action="update profile", object=f"user {user_id}",
        object_owner=user_id, required_permission="self-service email only", policy="field allowlist: email",
        decision="deny sensitive fields" if rejected else "allow", reason=(
            f"Trường không được phép: {', '.join(rejected)}" if rejected else "Chỉ email hợp lệ được cập nhật."
        ),
    )

