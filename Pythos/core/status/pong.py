from Pythos.core.utils.helpers import encode_varint
from Pythos.config.settings import MOTD
import json

async def pong(payload: bytes) -> bytes:
    motd_json = {
        "version": {
            "name": "1.21.5",
            "protocol": 754
        },
        "players": {
            "max": 20,
            "online": 0,
            "sample": []
        },
        "description": {
            "text": MOTD
        },
        "favicon": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAMAAACdt4HsAAAAAXNSR0IB2cksfwAAANVQTFRFAAAAAAAA////AgICBAQEDQ0NEBAQWFhYCwsLRkZGurq6FRUVJycnVVVVMTExGBgYXl5eeXl5GhoaLCwsBgYGEhISnJycwsHBNzc3ysrK19fXg4ODvb29NDQ0i4uLOjo6QkJCY2NjKSkpdnZ2TU1N5eXlJSUl9fX1lpaWoaGhzc3NISEhCAgIWltatra2xsbGSUlJ1NTU39/f3d3dkZGRa2trPz8/rKysUVFRZWVlh4eH0NDQr6+v7+/vHh4efX19cnJy6enp2tra8vLy+Pj4pKSks7OzqP1A3gAAAEd0Uk5TAP////////////////////////////////////////////////////////////////////////////////////////////8ihOZcAAAC20lEQVR4nO2VZ2/bQAyGS572lixLspblvR3vEc/YSf7/T+rZ7UfJ7bkoUBQhoAMl8B684h3Jb/CH9u0L8AX49wEEiMnz4D4LKOFhW1drU5w8CVj73XeAUPHCJwCEAIjTbLZNOtX4RD9wjIDqrnkUSlp6uIyd6rBt7HRGALSniBZEiHsIEFvVorhCgIXRGNsx3evg1L6+MgOU0yv42NlkM3yDqDZnBkQ4gzZuADTU4QXXzAAupadfEahXMcHolpkBdxvf9o35RyEPAE1L69QB3OtKF9kBdV1BxEPgksGcOqFYdI6FN/GEorBAeVCuHhQ1wTVhBEDLbgDMegBLpM/2XWAEcCivTahdAfpdmscENVYFMb5LtKAl6FhUCbZYiwlMpUavAAVcrwLIfqko7tE9IC2kudfmaD4IethQWj9SH1+eAljeu/XDW3V6NjtAtSO/17t5dvzhNYoOoRhAYFSBOa0FcuG6aWFHe5QDp5O+3QDhohMURz1KooX3X99gYTv6BeC37C8BDF3lk3JSajYdQ00EslShvcyvx3zAC7ZWU2/xiii+TCqZh740xw8GQEX3dR9lN4643UoZhdVwszPeciUUKJD7QUoLaX+G/ioe9du74LAcMCgY44yM6Cj4bIDfwUm/dJFEzB9uBQouKoiVO6Cv9PX+MSwZVosBMKUDxZrS8WRDGChiuJ1lbyOmHNA+flOwb0Ali6tn9OATIwYFws+FJ3SVOGjT1/wc5gJc4VZ8BDgOCA/STfldPXdfeZe4+QDivcjtQXNPGiPSC8wPtblwTyJ0a7RB7o/JgmwjrjbhvWPSE3IBw25PTgy5N0w1ySJ132muuYUBG9pLJFudNMD2uLPodEGOy7kA/tzIAiM78VFdSuua4oyU4XkIOm3Iw9dVtiR2l6RbNZXksZML4Eols1w2DcgmIA+GdcHUXJq5I9VLmrxacx0NggHUHL7O5wKesy/AF+A/AXwH7IpP00ShNWQAAAAASUVORK5CYII="
    }
    motd_str = json.dumps(motd_json, separators=(',', ':')).encode('utf-8')
    packet_id = encode_varint(0x00)
    json_length = encode_varint(len(motd_str))
    packet = packet_id + json_length + motd_str
    packet_length = encode_varint(len(packet))
    return packet_length + packet

async def pong2(payload: bytes) -> bytes:
    response_data = encode_varint(0x01) + payload  # Echo the timestamp
    response_packet = encode_varint(len(response_data)) + response_data
    return response_packet