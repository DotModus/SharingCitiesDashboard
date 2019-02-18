from http import HTTPStatus

from flask import jsonify
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from flask_restful import abort
from flask_restful import fields
from flask_restful import marshal
from flask_restful import reqparse
from sqlalchemy import exc

from db import db
from models.widget import WidgetModel


class Widgets(Resource):

    widget_fields = {"id": fields.Integer,
                     "userID": fields.Integer,
                     "type": fields.String,
                     "config": fields.String,
                     }

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('userID', required=True, help='userID required', location=['form', 'json'])
        self.reqparse.add_argument('type', required=True, help='type required', location=['form', 'json'])
        self.reqparse.add_argument('config', required=True, help='config required', location=['form', 'json'])


        # Delete args parser
        self.reqparse_delete = reqparse.RequestParser()
        self.reqparse_delete.add_argument('userID', required=True, help='A userID is required',
                                          location=['form', 'json'])
        self.reqparse_delete.add_argument('widgetID', required=True, help='widgetID required',
                                          location=['form', 'json'])

        # Get args parser
        self.req_get_parser = reqparse.RequestParser()
        self.req_get_parser.add_argument('userID', required=True, help='A user_id is required',
                                         location=['form', 'json'])
        self.req_get_parser.add_argument('limit', default=1, required=False, type=int,
                                         help='Limit needs to be an Integer', location=['form', 'json'])
        super().__init__()




    @jwt_required
    def get(self):
        """
        Gets a specified number of user widgets using the user identification number

        :argument
            Content-Type: Application/JSON
                ----- JSON keys -----
                userID - the users' unique identification number (Integer)
                limit - The number of Widgets to return (Integer) (Optional default value is 1)
        :return:
            Content-Type: Application/JSON
            widgetID - the widgets' unique identification number (Integer)
            user_id - the users' unique identification number (Integer)
            TODO: Add returned keys and desciptions
        """
        args = self.req_get_parser.parse_args()

        # Format the widgets that are returned for response
        widgets = (marshal(widget, self.widget_fields)
                   for widget in WidgetModel.query.filter_by(user_id=args["userID"]).limit(args["limit"]))
        # Create JSON serializable data format for response
        widgets_list = []
        for widget in widgets:
            widgets_list.append(widget)

        return jsonify({"widgets": widgets_list})



    @jwt_required
    def post(self):
        """
        Persists user Widget to the database

        :argument
            Content-Type: Application/JSON
                ----- JSON keys -----
                user_id - the users' unique identification number (Integer)
                TODO: Add returned keys and desciptions
        :return:
            Content-Type: Application/JSON
            TODO: Add returned keys and desciptions
        """
        args = self.reqparse.parse_args()

        if not args["type"] == "Plot" and not args["type"] == "Alert" and not args["type"] == "Map":
            abort(HTTPStatus.BAD_REQUEST.value, error="Invalid type: must be Plot, "
                                                      "Alert or Map.  type = {}".format(args["type"]))

        new_widget = WidgetModel(args["userID"], args["type"], args["config"])
        try:
            db.session.add(new_widget)
            db.session.commit()
        except exc.SQLAlchemyError:
            return jsonify(args), HTTPStatus.BAD_REQUEST.value

        return "Widget id {} Saved Succesfully".format(new_widget.id), HTTPStatus.OK.value


    @jwt_required
    def delete(self):
        """
         Deletes a user Widget from the database

        :argument
            Content-Type: Application/JSON
                ----- JSON keys -----
                user_id - the users' unique identification number (Integer)
                widget_id - the widgets unique identification number (Integer)
                TODO: Add returned keys and desciptions
        :return:
            Content-Type: Application/JSON
            TODO: Add returned keys and desciptions
        """
        args = self.reqparse_delete.parse_args()
        try:
            WidgetModel.query.filter_by(id=args["widgetID"]).delete()
            db.session.commit()
        except exc.SQLAlchemyError:
            abort(HTTPStatus.BAD_REQUEST.value)
        return "Widget id: {} deleted".format(args["widgetID"]), HTTPStatus.OK.value

    @classmethod
    def get_by_user_id(cls, user_id, widget_id):
        # Get widgets by user id
        return WidgetModel.query.filter_by(user_id=user_id, id=widget_id)









