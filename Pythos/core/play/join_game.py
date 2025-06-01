import struct
from Pythos.core.protocol import build_packet, encode_varint, encode_string, encode_nbt
from nbtlib import Compound, List, String, Int, Float, File

def to_nbt(obj):
    if isinstance(obj, dict):
        return Compound({k: to_nbt(v) for k, v in obj.items()})
    elif isinstance(obj, list):
        # Guess type: if empty, default to String; else use type of first element
        tag_type = type(obj[0]) if obj else String
        # Map Python types to nbtlib types
        py2nbt = {int: Int, float: Float, str: String, dict: Compound}
        nbt_tag = py2nbt.get(tag_type, String)
        return List[nbt_tag]([to_nbt(v) for v in obj])
    elif isinstance(obj, float):
        return Float(obj)
    elif isinstance(obj, int):
        return Int(obj)
    elif isinstance(obj, str):
        return String(obj)
    else:
        return obj

async def minimal_join_game_packet(entity_id: int = 1) -> bytes:
    """Builds a correct Join Game packet for Minecraft 1.16.5, field by field."""
    # --- Protocol fields (see wiki.vg/Protocol#Join_Game) ---
    # Entity ID (int)
    payload = bytearray(struct.pack(">i", entity_id))
    # Is Hardcore (bool)
    payload += struct.pack("?", False)
    # Gamemode (unsigned byte)
    payload += struct.pack("B", 1)  # Creative
    # Previous Gamemode (byte)
    payload += struct.pack("b", -1)  # None
    # World count (varint)
    payload += encode_varint(1)
    # World names (array of strings)
    payload += encode_string("minecraft:overworld")

    # --- Minimal valid dimension codec and dimension NBT for 1.16.5 ---
    dimension_codec = {
        "minecraft:dimension_type": {
            "type": "minecraft:dimension_type",
            "value": [
                {
                    "name": "minecraft:overworld",
                    "id": 0,
                    "element": {
                        "piglin_safe": 0,
                        "natural": 1,
                        "ambient_light": 1.0,
                        "infiniburn": "minecraft:infiniburn_overworld",
                        "respawn_anchor_works": 0,
                        "has_skylight": 1,
                        "bed_works": 1,
                        "effects": "minecraft:overworld",
                        "has_raids": 1,
                        "min_y": 0,
                        "height": 256,
                        "logical_height": 256,
                        "coordinate_scale": 1.0,
                        "ultrawarm": 0,
                        "has_ceiling": 0
                    }
                }
            ]
        },
        "minecraft:worldgen/biome": {
            "type": "minecraft:worldgen/biome",
            "value": []
        }
    }
    dimension = {
        "piglin_safe": 0,
        "natural": 1,
        "ambient_light": 1.0,
        "infiniburn": "minecraft:infiniburn_overworld",
        "respawn_anchor_works": 0,
        "has_skylight": 1,
        "bed_works": 1,
        "effects": "minecraft:overworld",
        "has_raids": 1,
        "min_y": 0,
        "height": 256,
        "logical_height": 256,
        "coordinate_scale": 1.0,
        "ultrawarm": 0,
        "has_ceiling": 0
    }
    # NBT encoding with root name ""
    payload += encode_nbt(File(to_nbt(dimension_codec)))
    payload += encode_nbt(File(to_nbt(dimension)))




    # World name (string)
    payload += encode_string("minecraft:overworld")
    # Hashed seed (long)
    payload += struct.pack(">q", 0)
    # Max players (varint)
    payload += encode_varint(10)
    # View distance (varint)
    payload += encode_varint(10)
    # Simulation distance (varint)
    payload += encode_varint(10)
    # Reduced debug info (bool)
    payload += struct.pack("?", False)
    # Enable respawn screen (bool)
    payload += struct.pack("?", True)
    # Is debug (bool)
    payload += struct.pack("?", False)
    # Is flat (bool)
    payload += struct.pack("?", True)
    return build_packet(0x24, bytes(payload))

def minimal_player_position_and_look_packet(x, y, z, yaw, pitch, teleport_id):
    packet_id = 0x00  # Check your protocol version!
    payload = struct.pack('>dddffB', x, y, z, yaw, pitch, 0)  # 0: flags (none)
    payload += encode_varint(teleport_id)
    return encode_varint(packet_id) + payload

# def minimal_join_game_packet(entity_id: int = 1, username: str = "Player") -> bytes:
#     payload = b""
#     payload += struct.pack(">i", entity_id)  # Entity ID
#     payload += struct.pack("?", False)       # Hardcore
#     payload += struct.pack("B", 1)           # Gamemode: Creative
#     payload += struct.pack("b", -1)          # Previous Gamemode: None

#     # World count + world name(s)
#     payload += encode_varint(1)
#     payload += encode_string("minecraft:overworld")

#     # Fake NBT data (normally complex) - sending empty compound here
#     empty_nbt = b'\x0a\x00\x00\x00'  # TAG_Compound + name (0 length) + end
#     payload += await encode_nbt(empty_nbt)  # You need to define await encode_nbt or just inline it

#     payload += await encode_nbt(empty_nbt)  # Dimension NBT (same dummy)

#     # World Name
#     payload += encode_string("minecraft:overworld")
#     payload += struct.pack(">q", 0)               # Hashed Seed
#     payload += encode_varint(10)                  # Max players
#     payload += encode_varint(10)                  # View distance
#     payload += encode_varint(10)                  # Simulation distance
#     payload += struct.pack("?", False)            # Reduced debug info
#     payload += struct.pack("?", True)             # Enable respawn screen
#     payload += struct.pack("?", False)            # Is debug
#     payload += struct.pack("?", True)             # Is flat

#     return build_packet(0x26, payload)
