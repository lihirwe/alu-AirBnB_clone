#!/usr/bin/python3
''' Unittest for FileStorage class
'''
import unittest
import json
import uuid
from datetime import datetime
from models import storage
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage


class TestFileStorageClass(unittest.TestCase):
    '''TestFileStorageClass tests the FileStorage class
    '''

    def test_file_path_is_private_from_instance(self):
        '''Test to ensure `__file_path` private
        class attribute is inaccessible from instance
        '''
        with self.assertRaises(AttributeError):
            file_path = storage.__file_path

    def test_file_path_is_private_from_class(self):
        '''Test to ensure `__file_path` private
        class attribute is inaccessible from class
        '''
        with self.assertRaises(AttributeError):
            file_path = FileStorage.__file_path

    def test_file_path_type(self):
        '''Test fails if `__file_path` private
        class attribute is not of type string
        '''
        self.assertIs(type(FileStorage._FileStorage__file_path), str)

    def test_objects_type(self):
        '''Test fails if `__objects` private
        class attribute is not of type dictionary
        '''
        self.assertIs(type(FileStorage._FileStorage__objects), dict)

    def test_all_return_type(self):
        '''Test fails if public instance method `all`
        does not return a dictionary of BaseModel instances
        '''
        for value in storage.all().values():
            self.assertIsInstance(value, BaseModel)

    def test_new_increases_count(self):
        '''Test ensures public instance method
        `new(obj)` increases the count of __objects
        '''
        prev_count = len(storage.all())
        test_model_0 = BaseModel(
            id=str(uuid.uuid4()),
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
        )
        storage.new(test_model_0)
        self.assertEqual(len(storage.all()), prev_count + 1)

    def test_new_accurate(self):
        '''Test ensures public instance method
        `new(obj)` accurately adds a new object to __objects
        '''
        test_model_0 = BaseModel(
            id=str(uuid.uuid4()),
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
        )
        storage.new(test_model_0)
        self.assertEqual(
            storage.all()[
                f"{test_model_0.__class__.__name__}.{test_model_0.id}"
            ].to_dict(),
            test_model_0.to_dict()
        )

    def test_objects_key_format(self):
        '''Test ensures all items in `__objects`
        private class attribute have correct key format
        '''
        test_model_1 = BaseModel()
        test_model_2 = BaseModel()
        objs = storage.all()
        for key in storage.all().keys():
            self.assertEqual(
                key,
                f"{objs[key].__class__.__name__}.{objs[key].id}"
            )

    def test_objects_value_type(self):
        '''Test ensures all items in `__objects`
        private class attribute are dictionaries
        '''
        test_model_3 = BaseModel()
        test_model_4 = BaseModel()
        for value in storage._FileStorage__objects.values():
            self.assertIsInstance(value, object)

    def test_save_serializes_correctly(self):
        '''Tests the public instance method `save`
        which serializes __objects correctly
        '''
        storage.save()
        with open(storage._FileStorage__file_path, 'r') as f:
            data = json.load(f)
            self.assertIsInstance(data, dict)
            self.assertEqual(data,
                             {key: value.to_dict() for key, value in
                              storage._FileStorage__objects.items()})

    def test_reload_deserializes_correctly(self):
        '''Tests the public instance method `reload`
        which deserializes __objects correctly
        '''
        prev_objs = storage._FileStorage__objects.copy()
        storage.save()
        test_model_5 = BaseModel(
            id=str(uuid.uuid4()),
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
        )
        storage.new(test_model_5)
        curr_objs = storage._FileStorage__objects.copy()
        storage.reload()
        self.assertNotEqual(len(prev_objs), len(curr_objs))
        self.assertNotEqual(storage._FileStorage__objects, curr_objs)
        self.assertNotEqual(storage._FileStorage__objects, prev_objs)


if __name__ == "__main__":
    unittest.main()
