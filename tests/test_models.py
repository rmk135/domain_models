"""Models tests."""

import datetime

import unittest2 as unittest

from domain_models import models
from domain_models import fields
from domain_models import collections
from domain_models import errors


class Photo(models.DomainModel):
    id = fields.Int()
    storage_path = fields.String()


class Profile(models.DomainModel):
    id = fields.Int()
    name = fields.String()
    main_photo = fields.Model(Photo)
    photos = fields.Collection(Photo)
    birth_date = fields.Date()


class BaseModelsTests(unittest.TestCase):
    """Basic model tests."""

    def test_set_and_get_attrs(self):
        """Test setting and getting of domain model attributes."""
        class User(models.DomainModel):
            """Test user domain model."""

            id = fields.Int()
            email = fields.String()
            first_name = fields.String()
            last_name = fields.String()
            gender = fields.String()
            birth_date = fields.String()

        user1 = User()
        user1.id = 1
        user1.email = 'example1@example.com'
        user1.first_name = 'John'
        user1.last_name = 'Smith'
        user1.gender = 'male'
        user1.birth_date = '05/04/1988'

        user2 = User()
        user2.id = 2
        user2.email = 'example2@example.com'
        user2.first_name = 'Jane'
        user2.last_name = 'Smith'
        user2.gender = 'female'
        user2.birth_date = '05/04/1985'

        self.assertEqual(user1.id, 1)
        self.assertEqual(user1.email, 'example1@example.com')
        self.assertEqual(user1.first_name, 'John')
        self.assertEqual(user1.last_name, 'Smith')
        self.assertEqual(user1.gender, 'male')
        self.assertEqual(user1.birth_date, '05/04/1988')

        self.assertEqual(user2.id, 2)
        self.assertEqual(user2.email, 'example2@example.com')
        self.assertEqual(user2.first_name, 'Jane')
        self.assertEqual(user2.last_name, 'Smith')
        self.assertEqual(user2.gender, 'female')
        self.assertEqual(user2.birth_date, '05/04/1985')

    def test_not_valid_unique_key_field(self):
        """Test that error is raised when unique key is not correct."""
        with self.assertRaises(errors.Error):
            class Model(models.DomainModel):
                """Test model."""

                __unique_key__ = fields.Field()

    def test_not_valid_unique_key_object(self):
        """Test that error is raised when unique key is not correct."""
        with self.assertRaises(errors.Error):
            class Model(models.DomainModel):
                """Test model."""

                __unique_key__ = object()

    def test_not_valid_unique_key_scalar(self):
        """Test that error is raised when unique key is not correct."""
        with self.assertRaises(errors.Error):
            class Model(models.DomainModel):
                """Test model."""

                __unique_key__ = 1

    def test_not_valid_view_key_field(self):
        """Test that error is raised when view key is not correct."""
        with self.assertRaises(errors.Error):
            class Model(models.DomainModel):
                """Test model."""

                __view_key__ = fields.Field()

    def test_not_valid_view_key_object(self):
        """Test that error is raised when view key is not correct."""
        with self.assertRaises(errors.Error):
            class Model(models.DomainModel):
                """Test model."""

                __view_key__ = object()

    def test_not_valid_view_key_scalar(self):
        """Test that error is raised when view key is not correct."""
        with self.assertRaises(errors.Error):
            class Model(models.DomainModel):
                """Test model."""

                __view_key__ = 1

    def test_field_could_not_be_rebound_in_same_model(self):
        """Test that field could not be rebound."""
        with self.assertRaises(errors.Error):
            class Model(models.DomainModel):
                """Test model."""

                field = fields.Field()
                another_field = field

    def test_field_could_not_be_rebound_in_different_model(self):
        """Test that field could not be rebound."""
        class Model1(models.DomainModel):
            """Test model."""

            field = fields.Field()

        with self.assertRaises(errors.Error):
            class Model2(models.DomainModel):
                """Test model."""

                field = Model1.field


class ModelSetterGetterTests(unittest.TestCase):
    """Tests for getter and setter methods of model."""
    data = {
        'id': 1,
        'name': 'John',
        'main_photo': {'id': 1,
                       'storage_path': 'some/dir/where/photos/live/1.jpg'},
        'photos': [
            {'id': 1, 'storage_path': 'some/dir/where/photos/live/1.jpg'},
            {'id': 2, 'storage_path': 'some/dir/where/photos/live/2.jpg'}
        ],
        'birth_date': datetime.date(year=1986, month=4, day=26)
    }

    def test_get_method_on_undefined(self):
        """Test method get of Model."""
        class Model(models.DomainModel):
            """Test model."""
            field = fields.Int()

        model = Model()

        with self.assertRaises(AttributeError):
            model.get('undefined')

    def test_get_method_on_int(self):
        """Test method get on Int of Model."""
        valid_defaults = [0, 3, 5.5, False, True]

        class Model(models.DomainModel):
            """Test model."""
            field = fields.Int()

        model = Model(field=2)
        for value in valid_defaults:
            self.assertEqual(model.get('field', default=value), 2)

        model = Model()
        self.assertEqual(model.get('field'), None)
        for value in valid_defaults:
            self.assertEqual(model.get('field', default=value), int(value))

        for value in ['', u'baz']:
            with self.assertRaises(ValueError):
                model.get('field', value)
                self.fail("Failed with {0}".format(value))

        with self.assertRaises(TypeError):
            model.get('field', object())

    def test_get_method_on_string(self):
        """Test method get on String of Model."""
        valid_defaults = ['', 'baz', u'baz', False, True, 1, 2.3]

        class Model(models.DomainModel):
            """Test model."""
            field = fields.String()

        model = Model(field='foobar')
        for value in valid_defaults:
            self.assertEqual(model.get('field', default=value), 'foobar')

        model = Model()
        self.assertEqual(model.get('field'), None)
        for value in valid_defaults:
            self.assertEqual(model.get('field', default=value), str(value))

    def test_get_method_on_bool(self):
        """Test method get on Bool of Model."""
        class Model(models.DomainModel):
            """Test model."""
            field = fields.Bool()

        model = Model(field=True)
        self.assertEqual(model.get('field'), True)
        self.assertEqual(model.get('field', default=False), True)

        model = Model(field=False)
        self.assertEqual(model.get('field'), False)
        self.assertEqual(model.get('field', default=True), False)

        model = Model()
        self.assertEqual(model.get('field'), None)
        self.assertEqual(model.get('field', default=False), False)
        self.assertEqual(model.get('field', default=True), True)

    def test_get_method_on_float(self):
        """Test method get on Float of Model."""
        valid_defaults = [7.5, 7, '7.5', '7', 0, '0.0', .9, '.9', False, True]

        class Model(models.DomainModel):
            """Test model."""
            field = fields.Float()

        model = Model(field=5.5)
        self.assertEqual(model.get('field'), 5.5)
        for value in valid_defaults:
            self.assertEqual(model.get('field', default=value), 5.5)

        model = Model()
        self.assertEqual(model.get('field'), None)
        for value in valid_defaults:
            self.assertEqual(model.get('field', default=value), float(value))

        for value in ['', 'baz', u'baz']:
            with self.assertRaises(ValueError):
                model.get('field', value)
                self.fail("Failed with {0}".format(value))

        with self.assertRaises(TypeError):
            model.get('field', object())

    def test_get_method_on_date(self):
        """Test method get on Date of Model."""
        once = datetime.date(year=1986, month=4, day=26)
        today = datetime.date.today()

        class Model(models.DomainModel):
            """Test model."""
            field = fields.Date()

        model = Model(field=today)
        self.assertEqual(model.get('field'), today)
        self.assertEqual(model.get('field', once), today)

        model = Model()
        self.assertEqual(model.get('field'), None)
        self.assertEqual(model.get('field', once), once)

        for value in ['', 'baz', u'baz', 0, 3, 0.7, '.5', False, True]:
            with self.assertRaises(TypeError):
                model.get('field', value)
                self.fail("Failed with {0}".format(value))

    def test_get_method_on_datetime(self):
        """Test method get on Date of Model."""
        once = datetime.datetime(year=1986, month=4, day=26)
        now = datetime.datetime.now()

        class Model(models.DomainModel):
            """Test model."""
            field = fields.DateTime()

        model = Model(field=now)
        self.assertEqual(model.get('field'), now)
        self.assertEqual(model.get('field', once), now)

        model = Model()
        self.assertEqual(model.get('field'), None)
        self.assertEqual(model.get('field', once), once)

        for value in ['', 'baz', u'baz', 0, 3, 0.7, '.5', False, True]:
            with self.assertRaises(TypeError):
                model.get('field', value)
                self.fail("Failed with {0}".format(value))

    def test_get_method_on_binary(self):
        """Test method get on Binary of Model."""
        self.skipTest("Test is not implemented yet")

    def test_get_method_on_model(self):
        """Test method get on Model of Model."""
        self.skipTest("Test is not implemented yet")

    def test_get_method_on_collection(self):
        """Test method get on Collection of Model."""
        self.skipTest("Test is not implemented yet")

    def test_get_data_method(self):
        """Test get_data method."""
        photo1 = Photo(id=1, storage_path='some/dir/where/photos/live/1.jpg')
        photo2 = Photo(id=2, storage_path='some/dir/where/photos/live/2.jpg')
        profile = Profile(id=1, name='John', main_photo=photo1,
                          photos=[photo1, photo2],
                          birth_date=datetime.date(year=1986, month=4,
                                                   day=26))

        self.assertDictEqual(profile.get_data(), self.data)

    def test_set_data_method(self):
        """Test set_data method."""
        profile = Profile()
        profile.set_data(self.data)

        self.assertEqual(profile.id, 1)
        self.assertEqual(profile.name, 'John')

        self.assertIsInstance(profile.main_photo, Photo)
        self.assertEqual(profile.main_photo.id, 1)
        self.assertEqual(profile.main_photo.storage_path,
                         'some/dir/where/photos/live/1.jpg')

        self.assertIsInstance(profile.photos, Photo.Collection)
        self.assertEqual(profile.photos[0].id, 1)
        self.assertEqual(profile.photos[0].storage_path,
                         'some/dir/where/photos/live/1.jpg')
        self.assertEqual(profile.photos[1].id, 2)
        self.assertEqual(profile.photos[1].storage_path,
                         'some/dir/where/photos/live/2.jpg')

        self.assertEqual(profile.birth_date,
                         datetime.date(year=1986, month=4, day=26))

    def test_set_data_via_constructor(self):
        """Test set data via model."""
        profile = Profile(**self.data)

        self.assertEqual(profile.id, 1)
        self.assertEqual(profile.name, 'John')

        self.assertIsInstance(profile.main_photo, Photo)
        self.assertEqual(profile.main_photo.id, 1)
        self.assertEqual(profile.main_photo.storage_path,
                         'some/dir/where/photos/live/1.jpg')

        self.assertIsInstance(profile.photos, Photo.Collection)
        self.assertEqual(profile.photos[0].id, 1)
        self.assertEqual(profile.photos[0].storage_path,
                         'some/dir/where/photos/live/1.jpg')
        self.assertEqual(profile.photos[1].id, 2)
        self.assertEqual(profile.photos[1].storage_path,
                         'some/dir/where/photos/live/2.jpg')

        self.assertEqual(profile.birth_date,
                         datetime.date(year=1986, month=4, day=26))

    def test_set_data_method_defaults(self):
        class Photo(models.DomainModel):
            id = fields.Int()
            storage_path = fields.String(
                default='some/dir/where/photos/live/default.jpg')

        default_photo = Photo()

        class Profile(models.DomainModel):
            id = fields.Int()
            name = fields.String()
            main_photo = fields.Model(Photo, default=default_photo)
            photos = fields.Collection(Photo)
            birth_date = fields.Date()
            something = fields.String(default='def-val')

        profile = Profile()
        profile.set_data({'id': 1, 'name': 'John'})

        self.assertEqual(profile.id, 1)
        self.assertEqual(profile.name, 'John')

        self.assertIsInstance(profile.main_photo, Photo)
        self.assertEqual(profile.main_photo.storage_path,
                         'some/dir/where/photos/live/default.jpg')

        self.assertIsNone(profile.main_photo.id)
        self.assertIsNone(profile.photos)
        self.assertIsNone(profile.birth_date)

        self.assertEqual(profile.something, 'def-val')

    def test_set_data_method_requirements(self):
        class Photo(models.DomainModel):
            id = fields.Int(required=True)
            storage_path = fields.String(required=True)

        class Profile(models.DomainModel):
            id = fields.Int()
            name = fields.String()
            main_photo = fields.Model(Photo)
            photos = fields.Collection(Photo)
            birth_date = fields.Date()

        profile = Profile()

        with self.assertRaises(AttributeError):
            profile.set_data({'main_photo': {'id': 1}})


class ModelReprTests(unittest.TestCase):
    """Tests for model Pythonic representation."""

    def test_repr(self):
        """Test model __repr__()."""
        class User(models.DomainModel):
            """Test user domain model."""

            id = fields.Int()
            email = fields.String()
            first_name = fields.String()
            last_name = fields.String()
            gender = fields.String()
            birth_date = fields.String()

        user = User()
        user.id = 1
        user.email = 'example1@example.com'
        user.first_name = 'John'
        user.last_name = 'Smith'
        user.gender = 'male'
        user.birth_date = '05/04/1988'

        user_repr = repr(user)

        self.assertIn('test_models.User', user_repr)
        self.assertIn('id=1', user_repr)
        self.assertIn('email=\'example1@example.com\'', user_repr)
        self.assertIn('first_name={0}'.format(repr('John')), user_repr)
        self.assertIn('last_name={0}'.format(repr('Smith')), user_repr)
        self.assertIn('gender=\'male\'', user_repr)
        self.assertIn('birth_date=\'05/04/1988\'', user_repr)


class ModelStrTests(unittest.TestCase):
    """Tests for model string representation."""

    def test_str_with_single_view_key(self):
        """Test model __str__()."""
        class User(models.DomainModel):
            """Test user domain model."""

            id = fields.Int()
            email = fields.String()
            first_name = fields.String()
            last_name = fields.String()
            gender = fields.String()
            birth_date = fields.String()

            __view_key__ = [id]

        user = User()
        user.id = 1
        user.email = 'example1@example.com'
        user.first_name = 'John'
        user.last_name = 'Smith'
        user.gender = 'male'
        user.birth_date = '05/04/1988'

        user_str = str(user)

        self.assertIn('test_models.User', user_str)
        self.assertIn('id=1', user_str)

        self.assertNotIn('example1@example.com', user_str)
        self.assertNotIn('John', user_str)
        self.assertNotIn('Smith', user_str)
        self.assertNotIn('male', user_str)
        self.assertNotIn('05/04/1988', user_str)

    def test_str_with_multiple_view_keys(self):
        """Test model __str__()."""
        class User(models.DomainModel):
            """Test user domain model."""

            id = fields.Int()
            email = fields.String()
            first_name = fields.String()
            last_name = fields.String()
            gender = fields.String()
            birth_date = fields.String()

            __view_key__ = (id, email)

        user = User()
        user.id = 1
        user.email = 'example1@example.com'
        user.first_name = 'John'
        user.last_name = 'Smith'
        user.gender = 'male'
        user.birth_date = '05/04/1988'

        user_str = str(user)

        self.assertIn('test_models.User', user_str)
        self.assertIn('id=1', user_str)
        self.assertIn('email=example1@example.com', user_str)

        self.assertNotIn('John', user_str)
        self.assertNotIn('Smith', user_str)
        self.assertNotIn('male', user_str)
        self.assertNotIn('05/04/1988', user_str)

    def test_str_without_view_key(self):
        """Test model __str__()."""
        class User(models.DomainModel):
            """Test user domain model."""

            id = fields.Int()
            email = fields.String()
            first_name = fields.String()
            last_name = fields.String()
            gender = fields.String()
            birth_date = fields.String()

        user = User()
        user.id = 1
        user.email = 'example1@example.com'
        user.first_name = 'John'
        user.last_name = 'Smith'
        user.gender = 'male'
        user.birth_date = '05/04/1988'

        self.assertEquals(str(user), repr(user))


class ModelSlotsOptimizationTests(unittest.TestCase):
    """Tests for model slots optimizations."""

    def test_model_slots(self):
        """Test model slots optimization."""
        class Model(models.DomainModel):
            """Test model."""

            field = fields.Field()

        test_model = Model()
        test_model.field = 'test'

        self.assertEquals(test_model.field, 'test')
        with self.assertRaises(AttributeError):
            test_model.undefined_field = 'NaN'

    def test_model_slots_disabling(self):
        """Test disabling of model slots optimization."""
        class Model(models.DomainModel):
            """Test model."""

            field = fields.Field()
            __slots_optimization__ = False

        test_model = Model()
        test_model.field = 'test'
        test_model.undefined_field = 'NaN'

        self.assertEquals(test_model.field, 'test')
        self.assertEquals(test_model.undefined_field, 'NaN')


class ModelsEqualityComparationsTests(unittest.TestCase):
    """Tests for models equality comparations."""

    def test_models_equal_single_key(self):
        """Test models equality comparator based on unique key."""
        class Model(models.DomainModel):
            """Test domain model with single unique key."""

            id = fields.Int()
            __unique_key__ = [id]

        user11 = Model()
        user11.id = 1

        user12 = Model()
        user12.id = 1

        self.assertTrue(user11 == user12)
        self.assertFalse(user11 != user12)

    def test_models_not_equal_single_key(self):
        """Test that models are not equal."""
        class Model(models.DomainModel):
            """Test domain model with single unique key."""

            id = fields.Int()
            __unique_key__ = [id]

        user1 = Model()
        user1.id = 1

        user2 = Model()
        user2.id = 2

        self.assertFalse(user1 == user2)
        self.assertTrue(user1 != user2)

    def test_models_equal_multiple_keys(self):
        """Test models equality comparator based on unique key."""
        class Model(models.DomainModel):
            """Test domain model with multiple unique key."""

            id = fields.Int()
            email = fields.String()
            __unique_key__ = (id, email)

        user11 = Model()
        user11.id = 1
        user11.email = 'john@example.com'

        user12 = Model()
        user12.id = 1
        user12.email = 'john@example.com'

        self.assertTrue(user11 == user12)
        self.assertFalse(user11 != user12)

    def test_models_not_equal_multiple_keys(self):
        """Test that models are not equal."""
        class Model(models.DomainModel):
            """Test domain model with multiple unique key."""

            id = fields.Int()
            email = fields.String()
            __unique_key__ = (id, email)

        user1 = Model()
        user1.id = 1
        user1.email = 'john@example.com'

        user2 = Model()
        user2.id = 2
        user2.email = 'jane@example.com'

        self.assertFalse(user1 == user2)
        self.assertTrue(user1 != user2)

    def test_models_not_equal_multiple_keys_first_equal(self):
        """Test that models are not equal."""
        class Model(models.DomainModel):
            """Test domain model with multiple unique key."""

            id = fields.Int()
            email = fields.String()
            __unique_key__ = (id, email)

        user11 = Model()
        user11.id = 1
        user11.email = 'john@example.com'

        user12 = Model()
        user12.id = 1
        user12.email = 'jane@example.com'

        self.assertFalse(user11 == user12)
        self.assertTrue(user11 != user12)

    def test_models_not_equal_different_classes(self):
        """Test that models are not equal."""
        class Model1(models.DomainModel):
            """Test domain model with single unique key."""

            id = fields.Int()
            __unique_key__ = [id]

        class Model2(models.DomainModel):
            """Test domain model with single unique key."""

            id = fields.Int()
            __unique_key__ = [id]

        user1 = Model1()
        user1.id = 1

        user2 = Model2()
        user2.id = 1

        self.assertFalse(user1 == user2)
        self.assertTrue(user1 != user2)

    def test_models_not_equal_scalar_value(self):
        """Test that model and scalar value are not equal."""
        class Model(models.DomainModel):
            """Test domain model with single unique key."""

            id = fields.Int()
            __unique_key__ = [id]

        user1 = Model()
        user1.id = 1

        self.assertFalse(user1 == 1)
        self.assertTrue(user1 != 1)

    def test_models_not_equal_unknown_unique_key(self):
        """Test that models are not equal."""
        class Model(models.DomainModel):
            """Test domain model without unique key."""

            id = fields.Int()

        user1 = Model()
        user1.id = 1

        user2 = Model()
        user2.id = 1

        self.assertFalse(user1 == user2)
        self.assertTrue(user1 != user2)

    def test_same_models_equal_unknown_unique_key(self):
        """Test that models are not equal."""
        class Model(models.DomainModel):
            """Test domain model without unique key."""

            id = fields.Int()

        user1 = Model()
        user1.id = 1

        self.assertTrue(user1 == user1)
        self.assertFalse(user1 != user1)

    def test_non_equal_models_in_set_single_key(self):
        """Test that non-equal models work properly with sets."""
        class Model(models.DomainModel):
            """Test domain model with single unique key."""

            id = fields.Int()
            __unique_key__ = [id]

        user1 = Model()
        user1.id = 1
        user2 = Model()
        user2.id = 2
        user3 = Model()
        user3.id = 3

        users_set = set((user1, user2, user3))

        self.assertEquals(len(users_set), 3)
        self.assertIn(user1, users_set)
        self.assertIn(user2, users_set)
        self.assertIn(user3, users_set)

    def test_equal_models_in_set_single_key(self):
        """Test that equal models work properly with sets."""
        class Model(models.DomainModel):
            """Test domain model with single unique key."""

            id = fields.Int()
            __unique_key__ = [id]

        user1 = Model()
        user1.id = 1
        user2 = Model()
        user2.id = 1
        user3 = Model()
        user3.id = 1

        users_set = set((user1, user2, user3))

        self.assertEquals(len(users_set), 1)
        self.assertIn(user1, users_set)
        self.assertIn(user2, users_set)
        self.assertIn(user3, users_set)

    def test_non_equal_models_in_set_multiple_keys(self):
        """Test that non-equal models work properly with sets."""
        class Model(models.DomainModel):
            """Test domain model with multiple unique key."""

            id = fields.Int()
            email = fields.String()
            __unique_key__ = (id, email)

        user1 = Model()
        user1.id = 1
        user1.email = 'email1@example.com'
        user2 = Model()
        user2.id = 2
        user2.email = 'email2@example.com'
        user3 = Model()
        user3.id = 3
        user3.email = 'email3@example.com'

        users_set = set((user1, user2, user3))

        self.assertEquals(len(users_set), 3)
        self.assertIn(user1, users_set)
        self.assertIn(user2, users_set)
        self.assertIn(user3, users_set)

    def test_equal_models_in_set_multiple_keys(self):
        """Test that equal models work properly with sets."""
        class Model(models.DomainModel):
            """Test domain model with multiple unique key."""

            id = fields.Int()
            email = fields.String()
            __unique_key__ = (id, email)

        user1 = Model()
        user1.id = 1
        user1.email = 'email1@example.com'
        user2 = Model()
        user2.id = 1
        user2.email = 'email1@example.com'
        user3 = Model()
        user3.id = 1
        user3.email = 'email1@example.com'

        users_set = set((user1, user2, user3))

        self.assertEquals(len(users_set), 1)
        self.assertIn(user1, users_set)
        self.assertIn(user2, users_set)
        self.assertIn(user3, users_set)

    def test_non_equal_models_in_set_without_unique_key(self):
        """Test that non-equal models work properly with sets."""
        class Model(models.DomainModel):
            """Test domain model without unique key."""

            id = fields.Int()

        user1 = Model()
        user1.id = 1
        user2 = Model()
        user2.id = 2
        user3 = Model()
        user3.id = 3

        users_set = set((user1, user2, user3))

        self.assertEquals(len(users_set), 3)
        self.assertIn(user1, users_set)
        self.assertIn(user2, users_set)
        self.assertIn(user3, users_set)

    def test_equal_models_in_set_without_unique_key(self):
        """Test that equal models work properly with sets."""
        class Model(models.DomainModel):
            """Test domain model without unique key."""

            id = fields.Int()

        user1 = Model()
        user1.id = 1
        user2 = user1
        user3 = user1

        users_set = set((user1, user2, user3))

        self.assertEquals(len(users_set), 1)
        self.assertIn(user1, users_set)
        self.assertIn(user2, users_set)
        self.assertIn(user3, users_set)

    def test_models_collection_extending(self):
        """Test model's collection extending."""
        class Credit(models.DomainModel):
            """Test credit domain model."""

            amount = fields.Int()

            class Collection(collections.Collection):
                """Credits collection."""

                @property
                def total_amount(self):
                    """Return sum of amounts of all contained credits."""
                    return sum(credit.amount for credit in self)

        credits = Credit.Collection([Credit(amount=1), Credit(amount=2)])

        self.assertEqual(credits.total_amount, 3)
