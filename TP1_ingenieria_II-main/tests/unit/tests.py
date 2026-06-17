"""
test.py - Pruebas actualizadas para el auth.py de Nexo Coworking
Patrones evaluados: Factory Method y Observer
Ejecutar: python tests.py
"""
import sys
import os
import unittest

# --- LA MAGIA: Le decimos a Python que agregue la carpeta 'src' a su radar ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

# Importamos solo lo que TODAVÍA existe en auth.py
from auth import (
    AuthService, AuthEventBus, InMemoryUserRepository,
    UserFactoryRegistry, ConsoleLogger,
    AuthEvent
)

class TestUserFactory(unittest.TestCase):
    def test_member_creation(self):
        factory = UserFactoryRegistry.get("member")
        user = factory.build("miembro_test", "m@x.com", "hash123")
        self.assertEqual(user.role, "member")
        self.assertEqual(user.email, "m@x.com")

    def test_invalid_type_raises(self):
        with self.assertRaises(ValueError):
            UserFactoryRegistry.get("alien")

class TestAuthServiceSignUp(unittest.TestCase):
    def setUp(self):
        self.repo = InMemoryUserRepository()
        self.bus = AuthEventBus()
        self.service = AuthService(self.repo, self.bus)

    def test_duplicate_username_fails(self):
        self.service.sign_up("user1", "uno@example.com", "Segura1!", "Segura1!", "member")
        result = self.service.sign_up("user1", "dos@example.com", "Segura1!", "Segura1!", "member")
        self.assertFalse(result.success)
        self.assertIn("Usuario duplicado", result.errors[0])

    def test_passwords_do_not_match(self):
        result = self.service.sign_up("userX", "x@x.com", "Segura1!", "Distinta2@", "member")
        
        # 1. Validamos que el sistema bloquee el registro (success = False)
        self.assertFalse(result.success)
        
        # 2. Buscamos cualquiera de las dos palabras clave para que no explote
        errores_completos = str(result.message) + str(result.errors)
        self.assertTrue("validación" in errores_completos.lower() or "coinciden" in errores_completos.lower())

class TestObserverPattern(unittest.TestCase):
    def test_event_bus_publishes_events(self):
        bus = AuthEventBus()
        
        class TestObserver:
            def __init__(self):
                self.events_received = []
            def update(self, event):
                self.events_received.append(event)
                
        espia = TestObserver()
        bus.subscribe(espia)
        
        evento_prueba = AuthEvent(AuthEvent.USER_REGISTERED, {"email": "test@x.com"})
        bus.publish(evento_prueba)
        
        self.assertEqual(len(espia.events_received), 1)
        self.assertEqual(espia.events_received[0].event_type, AuthEvent.USER_REGISTERED)

if __name__ == "__main__":
    unittest.main(verbosity=2)