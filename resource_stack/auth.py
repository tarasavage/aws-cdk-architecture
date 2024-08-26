from aws_cdk import (
    aws_cognito as _cognito,
    RemovalPolicy,
)
from constructs import Construct


class CognitoConstruct(Construct):
    def __init__(self, scope: Construct, construct_id: str) -> None:
        super().__init__(scope, construct_id)

        self._user_pool = _cognito.UserPool(
            self, "UserPool",
            user_pool_name="DragonUserPool",
            self_sign_up_enabled=True,
            sign_in_aliases=_cognito.SignInAliases(email=True),
            auto_verify=_cognito.AutoVerifiedAttrs(email=True),
            standard_attributes=_cognito.StandardAttributes(
                email=_cognito.StandardAttribute(required=True),
            ),
            account_recovery=_cognito.AccountRecovery.EMAIL_ONLY,
            mfa=_cognito.Mfa.OFF,
            password_policy=_cognito.PasswordPolicy(
                min_length=8,
                require_lowercase=True,
                require_uppercase=True,
                require_digits=True,
                require_symbols=False,
            ),
            removal_policy=RemovalPolicy.DESTROY,
        )

        self._domain = self._user_pool.add_domain(
            "CognitoDomain",
            cognito_domain=_cognito.CognitoDomainOptions(
                domain_prefix="dragon-auth"
            )
        )

    @property
    def user_pool(self) -> _cognito.UserPool:
        return self._user_pool


class CognitoClientConstruct(Construct):
    def __init__(
            self, scope: Construct,
            construct_id: str,
            user_pool: _cognito.UserPool,
            callback_urls: list[str],
    ) -> None:
        super().__init__(scope, construct_id)

        self._user_pool_client = _cognito.UserPoolClient(
            self, "DragonUserPoolClient",
            user_pool=user_pool,
            user_pool_client_name="DragonUserPoolClient",
            generate_secret=False,
            auth_flows=_cognito.AuthFlow(
                user_password=True,
                user_srp=True,
            ),
            o_auth=_cognito.OAuthSettings(
                flows=_cognito.OAuthFlows(
                    implicit_code_grant=True,
                ),
                scopes=[
                    _cognito.OAuthScope.EMAIL,
                    _cognito.OAuthScope.OPENID,
                    _cognito.OAuthScope.PROFILE,
                ],
                callback_urls=callback_urls,
            ),
        )

    @property
    def user_pool_client(self) -> _cognito.UserPoolClient:
        return self._user_pool_client
