from fastapi import Depends, HTTPException, status
from app.api.deps import get_current_user

def require_role(required_role: str):
    def role_checker(current_user: dict = Depends(get_current_user)):
        user_role = current_user.get("role")
        
        if user_role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
            
        return current_user
    
    
    return role_checker