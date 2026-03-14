from fastapi import APIRouter, Depends
from app.models.schemas import AdminAuthRequest, AdminAuthResponse, AdminStats, AdminUserResponse, ProjectTestCaseCount
from fastapi.responses import RedirectResponse
from app.services.auth import admin_auth, verify_admin_session
from typing import List, Optional

router = APIRouter()


@router.api_route(
    path="/login",
    response_model=AdminAuthResponse,
    summary="For admin to login",
    description="Admin enters in a fixed username and password, returns a session token 5 hours limit",
    responses={
        200: {"model": AdminAuthResponse, "description": "Successfully login"},
        401: {"model": AdminAuthResponse, "description": "Unauthorized"},
    },
    deprecated=False,
    methods=["POST"],
)
async def admin_login(request: AdminAuthRequest):
    result = await admin_auth(request=request)

    return result


@router.get(
    "/stats",
    response_model=AdminStats,
    summary="Get admin dashboard stats",
)
async def get_stats(session=Depends(verify_admin_session)):
    # Mock data to match mobile requirements
    return AdminStats(
        totalUsers=1,
        activeUsers=1,
        deletedUsers=0,
        totalTestCases=10,
        projectTestCases=[
            ProjectTestCaseCount(projectKey="DEMO", projectName="Demo Project", count=10)
        ]
    )


@router.get(
    "/users",
    response_model=List[AdminUserResponse],
    summary="Get all users",
)
async def get_users(session=Depends(verify_admin_session)):
    # Mock data to match mobile requirements
    return [
        AdminUserResponse(
            id="1",
            name="Admin User",
            email="admin@example.com",
            role="admin",
            isActive=True,
            createdAt="2024-03-12T00:00:00Z"
        )
    ]


@router.get(
    "/testcases",
    summary="Get admin test cases",
)
@router.get(
    "/test-cases",
    summary="Get admin test cases (alias)",
)
async def get_admin_testcases(
    projectKey: Optional[str] = None,
    session=Depends(verify_admin_session),
):
    # Mock data compatible with mobile AdminTestCase type.
    data = [
        {
            "id": "case-1",
            "projectKey": "DEMO",
            "projectName": "Demo Project",
            "issueKey": "DEMO-101",
            "requirement": "Login success flow should return 200 and auth token",
            "tests": [
                {
                    "id": "t-1",
                    "title": "Valid login",
                    "type": "Functional",
                    "description": "User logs in with valid credentials",
                    "steps": [
                        "POST /api/auth/login with valid username/password",
                        "Verify response status is 200",
                        "Verify token exists in response body",
                    ],
                    "url": "/api/auth/login",
                    "method": "POST",
                }
            ],
            "createdAt": "2025-03-03T00:00:00Z",
        },
        {
            "id": "case-2",
            "projectKey": "DEMO",
            "projectName": "Demo Project",
            "issueKey": "DEMO-102",
            "requirement": "Invalid password should return 401",
            "tests": [
                {
                    "id": "t-2",
                    "title": "Invalid password",
                    "type": "Negative",
                    "description": "Login should fail with wrong password",
                    "steps": [
                        "POST /api/auth/login with wrong password",
                        "Verify response status is 401",
                        "Verify error message is returned",
                    ],
                    "url": "/api/auth/login",
                    "method": "POST",
                }
            ],
            "createdAt": "2025-03-04T00:00:00Z",
        },
        {
            "id": "case-3",
            "projectKey": "PAY",
            "projectName": "Payment Service",
            "issueKey": "PAY-55",
            "requirement": "Create payment intent should return 200",
            "tests": [
                {
                    "id": "t-3",
                    "title": "Create payment intent",
                    "type": "Integration",
                    "description": "Backend creates payment intent",
                    "steps": [
                        "POST /api/payments/create-intent",
                        "Verify response status is 200",
                        "Verify client_secret is present",
                    ],
                    "url": "/api/payments/create-intent",
                    "method": "POST",
                }
            ],
            "createdAt": "2025-03-05T00:00:00Z",
        },
    ]

    if projectKey:
        return [d for d in data if d["projectKey"].upper() == projectKey.upper()]
    return data
