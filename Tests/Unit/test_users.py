# Testes (1 ao 20) desenvolvidos por Henrique Souza
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import unittest
from unittest.mock import MagicMock
from Models.user import User
from Services.user_service import create_user


class TestUserService(unittest.TestCase):

    def setUp(self):
        """
        CONFIGURAÇÃO INICIAL DO TESTE
        Criamos um mock do banco de dados
        """
        self.db = MagicMock()

    # =========================================================
    # TESTE 1
    # =========================================================
    def test_1_create_user_success(self):
        """
        TESTE 1: Criar usuário com sucesso
        """

        # 1 - CRIANDO CENÁRIO DE TESTE
        self.db.query().filter().first.return_value = None

        # 2 - EXECUÇÃO
        result = create_user(self.db, "manson", "Password123", "admin")

        # 3 - VALIDAÇÃO
        self.assertEqual(result.username, "manson")
        self.db.add.assert_called_once()
        self.db.commit.assert_called_once()

    # =========================================================
    # TESTE 2
    # =========================================================
    def test_2_create_user_duplicate(self):
        """
        TESTE 2: Usuário duplicado
        """

        # 1 - CENÁRIO
        self.db.query().filter().first.return_value = User(
            username="manson", password="Password123", role="admin"
        )

        # 2 - EXECUÇÃO
        with self.assertRaises(Exception):
            create_user(self.db, "manson", "Password123", "admin")

        # 3 - VALIDAÇÃO
        self.db.add.assert_not_called()

    # =========================================================
    # TESTE 3
    # =========================================================
    def test_3_password_without_number(self):
        """
        TESTE 3: Senha sem número
        """

        # 1 - CENÁRIO
        self.db.query().filter().first.return_value = None

        # 2 - EXECUÇÃO
        with self.assertRaises(Exception):
            create_user(self.db, "manson", "Password", "admin")

        # 3 - VALIDAÇÃO
        self.db.commit.assert_not_called()

    # =========================================================
    # TESTE 4
    # =========================================================
    def test_4_password_without_uppercase(self):
        """
        TESTE 4: Senha sem maiúscula
        """

        # 1 - CENÁRIO
        self.db.query().filter().first.return_value = None

        # 2 - EXECUÇÃO
        with self.assertRaises(Exception):
            create_user(self.db, "manson", "password123", "admin")

        # 3 - VALIDAÇÃO
        self.db.add.assert_not_called()

    # =========================================================
    # TESTE 5
    # =========================================================
    def test_5_password_too_short(self):
        """
        TESTE 5: Senha curta
        """

        # 1 - CENÁRIO
        self.db.query().filter().first.return_value = None

        # 2 - EXECUÇÃO
        with self.assertRaises(Exception):
            create_user(self.db, "manson", "P1a", "admin")

        # 3 - VALIDAÇÃO
        self.db.commit.assert_not_called()

    # =========================================================
    # TESTE 6
    # =========================================================
    def test_6_username_empty(self):
        """
        TESTE 6: Username vazio
        """

        # 1 - CENÁRIO
        self.db.query().filter().first.return_value = None

        # 2 - EXECUÇÃO
        with self.assertRaises(Exception):
            create_user(self.db, "", "Password123", "admin")

        # 3 - VALIDAÇÃO
        self.db.add.assert_not_called()

    # =========================================================
    # TESTE 7
    # =========================================================
    def test_7_role_default(self):
        """
        TESTE 7: Role padrão
        """

        # 1 - CENÁRIO
        self.db.query().filter().first.return_value = None

        # 2 - EXECUÇÃO
        result = create_user(self.db, "manson", "Password123", None)

        # 3 - VALIDAÇÃO
        self.assertIsNotNone(result)

    # =========================================================
    # TESTE 8
    # =========================================================
    def test_8_multiple_users(self):
        """
        TESTE 8: Criar múltiplos usuários
        """

        # 1 - CENÁRIO
        self.db.query().filter().first.return_value = None

        # 2 - EXECUÇÃO
        create_user(self.db, "user1", "Password123", "admin")
        create_user(self.db, "user2", "Password123", "admin")

        # 3 - VALIDAÇÃO
        self.assertEqual(self.db.add.call_count, 2)

    # =========================================================
    # TESTE 9
    # =========================================================
    def test_9_commit_called(self):
        """
        TESTE 9: Commit chamado
        """

        # 1 - CENÁRIO
        self.db.query().filter().first.return_value = None

        # 2 - EXECUÇÃO
        create_user(self.db, "manson", "Password123", "admin")

        # 3 - VALIDAÇÃO
        self.db.commit.assert_called_once()

    # =========================================================
    # TESTE 10
    # =========================================================
    def test_10_add_called(self):
        """
        TESTE 10: Add chamado
        """

        # 1 - CENÁRIO
        self.db.query().filter().first.return_value = None

        # 2 - EXECUÇÃO
        create_user(self.db, "manson", "Password123", "admin")

        # 3 - VALIDAÇÃO
        self.db.add.assert_called_once()

    # =========================================================
    # TESTE 11
    # =========================================================
    def test_11_username_with_spaces(self):
        """
        TESTE 11: Username com espaço
        """

        # 1 - CENÁRIO
        self.db.query().filter().first.return_value = None

        # 2 - EXECUÇÃO
        result = create_user(self.db, "man son", "Password123", "admin")

        # 3 - VALIDAÇÃO
        self.assertIsNotNone(result)

    # =========================================================
    # TESTE 12
    # =========================================================
    def test_12_password_with_special_char(self):
        """
        TESTE 12: Senha com caractere especial
        """

        # 1 - CENÁRIO
        self.db.query().filter().first.return_value = None

        # 2 - EXECUÇÃO
        result = create_user(self.db, "manson", "Password@123", "admin")

        # 3 - VALIDAÇÃO
        self.assertIsNotNone(result)

    # =========================================================
    # TESTE 13
    # =========================================================
    def test_13_null_password(self):
        """
        TESTE 13: Senha nula
        """

        # 1 - CENÁRIO
        self.db.query().filter().first.return_value = None

        # 2 - EXECUÇÃO
        with self.assertRaises(Exception):
            create_user(self.db, "manson", None, "admin")

        # 3 - VALIDAÇÃO
        self.db.add.assert_not_called()

    # =========================================================
    # TESTE 14
    # =========================================================
    def test_14_null_username(self):
        """
        TESTE 14: Username nulo
        """

        # 1 - CENÁRIO
        self.db.query().filter().first.return_value = None

        # 2 - EXECUÇÃO
        with self.assertRaises(Exception):
            create_user(self.db, None, "Password123", "admin")

        # 3 - VALIDAÇÃO
        self.db.add.assert_not_called()

    # =========================================================
    # TESTE 15
    # =========================================================
    def test_15_role_none(self):
        """
        TESTE 15: Role None vira padrão
        """

        # 1 - CENÁRIO
        self.db.query().filter().first.return_value = None

        # 2 - EXECUÇÃO
        result = create_user(self.db, "manson", "Password123", None)

        # 3 - VALIDAÇÃO
        self.assertIsNotNone(result)

    # =========================================================
    # TESTE 16
    # =========================================================
    def test_16_db_rollback_not_called(self):
        """
        TESTE 16: Rollback não deve ser chamado
        """

        # 1 - CENÁRIO
        self.db.query().filter().first.return_value = None

        # 2 - EXECUÇÃO
        create_user(self.db, "manson", "Password123", "admin")

        # 3 - VALIDAÇÃO
        self.db.rollback.assert_not_called()

    # =========================================================
    # TESTE 17
    # =========================================================
    def test_17_user_object_created(self):
        """
        TESTE 17: Retorna objeto User
        """

        # 1 - CENÁRIO
        self.db.query().filter().first.return_value = None

        # 2 - EXECUÇÃO
        result = create_user(self.db, "manson", "Password123", "admin")

        # 3 - VALIDAÇÃO
        self.assertIsInstance(result, User)

    # =========================================================
    # TESTE 18
    # =========================================================
    def test_18_commit_called_once(self):
        """
        TESTE 18: Commit chamado uma vez
        """

        # 1 - CENÁRIO
        self.db.query().filter().first.return_value = None

        # 2 - EXECUÇÃO
        create_user(self.db, "manson", "Password123", "admin")

        # 3 - VALIDAÇÃO
        self.assertEqual(self.db.commit.call_count, 1)

    # =========================================================
    # TESTE 19
    # =========================================================
    def test_19_add_called_once(self):
        """
        TESTE 19: Add chamado uma vez
        """

        # 1 - CENÁRIO
        self.db.query().filter().first.return_value = None

        # 2 - EXECUÇÃO
        create_user(self.db, "manson", "Password123", "admin")

        # 3 - VALIDAÇÃO
        self.assertEqual(self.db.add.call_count, 1)

    # =========================================================
    # TESTE 20
    # =========================================================
    def test_20_no_duplicate_add(self):
        """
        TESTE 20: Não adicionar usuário duplicado
        """

        # 1 - CENÁRIO
        self.db.query().filter().first.return_value = User(
            username="manson", password="Password123", role="admin"
        )

        # 2 - EXECUÇÃO
        with self.assertRaises(Exception):
            create_user(self.db, "manson", "Password123", "admin")

        # 3 - VALIDAÇÃO
        self.assertEqual(self.db.add.call_count, 0)


if __name__ == "__main__":
    unittest.main()
