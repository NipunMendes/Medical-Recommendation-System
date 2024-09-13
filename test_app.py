import unittest
from main import app, get_predicted_value, helper
import mysql.connector
from werkzeug.security import generate_password_hash


class FlaskAppTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db_config = {
            'user': 'root',
            'password': '',
            'host': 'localhost',
            'database': 'test_medical_app'
        }
        cls.conn = mysql.connector.connect(**cls.db_config)
        cls.cursor = cls.conn.cursor()

        # Create users table if it doesn't exist
        cls.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(100) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL
            )
        ''')
        cls.conn.commit()

        # Insert a test user with hashed password
        hashed_password = generate_password_hash('correct_password')
        cls.cursor.execute('INSERT IGNORE INTO users (username, password) VALUES (%s, %s)',
                           ('test_user', hashed_password))
        cls.conn.commit()

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()  # Close the database connection

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_home_redirect(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 302)  # Redirect to /login

    def test_login_correct(self):
        response = self.app.post('/login', data=dict(username='test_user', password='correct_password'),
                                 follow_redirects=True)
        self.assertEqual(response.status_code, 200)  # Ensure the login was successful with status code 200

    def test_login_incorrect(self):
        response = self.app.post('/login', data=dict(username='test_user', password='wrong_password'),
                                 follow_redirects=True)
        self.assertIn(b'Invalid username or password', response.data)  # Check error message

    def test_prediction(self):
        symptoms = ['itching', 'fatigue']
        predicted_disease = get_predicted_value(symptoms)
        self.assertEqual(predicted_disease, 'Fungal infection')  # Adjust based on the model

    def test_helper_function(self):
        description, precautions, medications, diets, workouts = helper('Fungal infection')
        self.assertTrue(description)
        self.assertTrue(precautions)


if __name__ == '__main__':
    unittest.main()
