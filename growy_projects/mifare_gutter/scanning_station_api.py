from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from uart_com import SerialToScale
from py532lib.mifare_gutter import *


card = MifareGutter()
card.SAMconfigure()
card.set_max_retries(MIFARE_WAIT_FOR_ENTRY)

scale = SerialToScale()

#uid = card.scan_field()
CLCK_GUTTER = "CLCK"

app = Flask(__name__)
api = Api(app)

initGutter_post_args = reqparse.RequestParser()
initGutter_post_args.add_argument("RFID", type=str, help="{RFID: ....} is required in application/json", required=True)
initGutter_post_args.add_argument("gutterType", type=str, help="{gutterType: ....}application/json", default=CLCK_GUTTER)
initGutter_post_args.add_argument("gutterNetWeight", type=str, help="{gutterNetWeight: ....}application/json", required=True)

gutterinfo= ['PLASTIC','2834','2','2211132211']
uid= '04:21:47:2A:44:70:80'
scale_weight = "2873"



class GetInfo(Resource):
    def get(self):
        uid = card.scan_field()
        gutterinfo = card.gutter_info()

        info = {"tag": {"RFID": uid,
                        "gutterType": gutterinfo[0],
                        "gutterNetWeight": gutterinfo[1],
                        "gutterUsageCounter": gutterinfo[2],
                        "initTimestamp": gutterinfo[3]
                        },
                "scale": scale.return_weight().decode()
                }
        return info


class InitGutter(Resource):

    def put(self):
        args = initGutter_post_args.parse_args()
        uid = card.scan_field()
        if args["RFID"] == uid:
<<<<<<< HEAD
            card.set_netweight_gutter(args["gutterNetWeight"].encode())
            card.set_gutter_type(args["gutterType"].encode())
=======
            card.set_baseweight_gutter()
            card.set_gutter_type()
>>>>>>> af5ee5f (no message)
            card.set_datetime()
        print(args)
        return {"tag":args}


class Increment(Resource):
    def get(self):
        return 0

class Tare(Resource):
    def get(self):
        scale.send_tare()
        info = {"scale": scale.return_weight().decode()}
        return info
        

api.add_resource(GetInfo, "/api")
api.add_resource(InitGutter, "/api/initGutter")
api.add_resource(Increment, "/api/increment")
api.add_resource(Tare, "/api/tare")

if __name__ == "__main__":
    app.run(debug=True)



