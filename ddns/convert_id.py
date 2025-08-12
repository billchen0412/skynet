import base64
import csv
import re

import requests

# UUID regex pattern
uuid_pattern = re.compile(
    r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b"
)


def encode_varint(value: int) -> bytes:
    """Encode an int using protobuf varint format (LEB128)"""
    result = bytearray()
    while value > 0x7F:
        result.append((value & 0x7F) | 0x80)
        value >>= 7
    result.append(value)
    return bytes(result)


def build_convert_face_id_payload(profile_id: int) -> str:
    # 1. Varint encode the profile ID
    varint_encoded = encode_varint(profile_id)

    # 2. Protobuf field 1 (tag 0x0A), wire type 2 (length-delimited), then length of varint + value
    proto_msg = b"\x0a" + bytes([len(varint_encoded)]) + varint_encoded

    # 3. gRPC-Web adds 5-byte header: 1-byte compression flag (0), then 4-byte big-endian length
    grpc_header = b"\x00" + len(proto_msg).to_bytes(4, byteorder="big")

    # 4. Final payload
    full_payload = grpc_header + proto_msg

    # 5. Base64 encode it for gRPC-web-text
    return base64.b64encode(full_payload).decode("utf-8")


def get_face_id(profile_id: int):
    payload = build_convert_face_id_payload(profile_id)

    headers = {
        "accept": "application/grpc-web-text",
        "content-type": "application/grpc-web-text",
        "origin": "https://jkface.net",
        "referer": "https://jkface.net/",
        "x-grpc-web": "1",
        "x-user-agent": "grpc-web-javascript/0.1",
    }

    url = "https://face-front-api.hare200.com/gapi/face.v2.FaceService/ConvertFaceId"
    response = requests.post(url, headers=headers, data=payload)

    if response.status_code == 200:
        b64_str = response.text

        # Split if gRPC-Web trailer is appended (as in your example)
        main_payload = b64_str.split("=")[0] + "=" * (
            4 - len(b64_str.split("=")[0]) % 4
        )  # ensure padding

        try:
            raw_bytes = base64.b64decode(main_payload)
            text = raw_bytes.decode("utf-8", errors="ignore")

            # Search for UUID pattern
            match = uuid_pattern.search(text)
            if match:
                print(f"✅ Found ID: ${match.group(0)}")
                return match.group(0)
            else:
                print("❌ No ID found")

        except Exception as e:
            print(f"❌ Failed to decode: {e}")
    else:
        print(f"❌ Request failed: {response.status_code}")
        print(response.text)
    return None


def build_get_face_profile_payload(face_id: str) -> str:
    """
    Given a UUID face ID string, generate gRPC-Web base64-encoded payload
    for GetFaceProfile.
    """
    # 1. Convert UUID string to UTF-8 bytes
    face_id_bytes = face_id.encode("utf-8")
    length = len(face_id_bytes)

    # 2. Protobuf field 1 (tag = 0x0A), length-delimited
    proto_body = b"\x0a" + bytes([length]) + face_id_bytes

    # 3. gRPC-Web header: 1 byte (0x00) + 4-byte big-endian length
    grpc_header = b"\x00" + len(proto_body).to_bytes(4, byteorder="big")

    # 4. Combine and encode to base64
    full_payload = grpc_header + proto_body
    return base64.b64encode(full_payload).decode("utf-8")


def extract_social_links_from_response(base64_response: str) -> list:
    """
    Decode gRPC-Web base64 response and extract social links.
    """
    try:
        # Step 1: Decode base64
        decoded = base64.b64decode(base64_response)

        # Step 2: gRPC-Web message(s) may be framed like:
        # [1-byte compression flag][4-byte message length][message...]
        links = []
        i = 0
        while i < len(decoded):
            if i + 5 > len(decoded):
                break
            # Read gRPC frame
            compressed_flag = decoded[i]
            message_len = int.from_bytes(decoded[i + 1 : i + 5], byteorder="big")
            message = decoded[i + 5 : i + 5 + message_len]

            # Try to extract readable parts (as fallback heuristic)
            try:
                text = message.decode("utf-8", errors="ignore")
                urls = re.findall(r'https?://[^\s"\'<>]+', text)
                # Filter common social/profile links
                urls = [
                    u
                    for u in urls
                    if any(
                        domain in u
                        for domain in ["instagram.com", "jvid.com", "jkface.net"]
                    )
                ]
                links.extend(urls)
            except:
                pass

            i += 5 + message_len

        return list(dict.fromkeys(links))  # remove duplicates while preserving order

    except Exception as e:
        print("❌ Failed to parse:", e)
        return []


def fetch_face_profile(face_id: str) -> list:
    payload = build_get_face_profile_payload(face_id)

    headers = {
        "accept": "application/grpc-web-text",
        "content-type": "application/grpc-web-text",
        "origin": "https://jkface.net",
        "referer": "https://jkface.net/",
        "x-grpc-web": "1",
        "x-user-agent": "grpc-web-javascript/0.1",
        "user-agent": "Mozilla/5.0",
    }

    url = "https://face-front-api.hare200.com/gapi/face.v2.FaceService/GetFaceProfile"
    response = requests.post(url, headers=headers, data=payload)

    if response.status_code == 200:
        return extract_social_links_from_response(response.text)
    else:
        print(
            f"❌ Failed to fetch profile for {face_id}. Status code: {response.status_code}"
        )
        return []


profile_ids = [
    # 5903274,
    # 6070262,
    # 5846607,
    # 6063177,
    # 6059007,
    5675902,
    5846923,
    5847085,
    5888976,
    5846909,
    5846926,
    5888980,
    5845129,
    5564317,
    5847086,
    5647098,
    6038846,
    6038847,
    6038848,
    5846911,
    5932209,
    5925808,
    5888974,
    5847089,
    5925807,
    5846915,
    5903295,
    5888987,
    5903307,
    5903311,
    5888986,
    5903547,
    5903304,
    5997737,
    6038724,
    5888983,
    2837029,
    6057547,
    5888965,
    6055368,
    5888975,
    6055369,
    5888981,
    6040236,
    6040234,
    6071232,
    5903291,
    6067527,
    5846908,
    5847088,
    5903312,
    6069146,
    6069147,
    6040242,
    6040197,
    5888971,
    6040211,
    5967402,
    5903289,
    6062266,
    6062265,
    5903298,
    6068834,
    5903309,
    5925817,
    5903321,
    5967418,
    5888972,
    6057545,
    6040232,
    5967395,
    5932210,
    6038723,
    5846620,
    6068806,
    6068805,
    6068803,
    6073693,
    6073694,
    5903300,
    6074209,
    6074210,
    6040201,
    6076615,
    6040203,
    6078841,
    6078840,
    6078839,
    5888984,
    5903313,
    6000018,
    6000012,
    6057534,
    5846570,
    6038832,
    6062254,
    5846576,
    5846577,
    6000010,
    6058762,
    6062259,
    5932213,
    6057535,
    4398776,
    6066206,
    6066207,
    6063221,
    6066208,
    5846607,
    6063177,
    5846580,
    6059007,
    5846567,
    6059006,
    6059005,
    4398585,
    6067842,
    6063223,
    5903274,
    6066301,
    6067844,
    6070262,
    6077996,
    5846585,
    6063222,
    6058761,
    5846584,
    5846588,
    5846583,
    5846586,
    5846582,
    6063220,
    6070222,
    5331996,
    6081337,
    6079109,
    5908113,
    5934527,
    6073000,
    6072987,
    6072963,
    6078797,
    5711953,
    5533279,
    5753161,
    4398590,
    6056782,
    5991106,
    4847389,
    5999935,
    6075571,
    5999948,
    6075572,
    6075573,
    6075575,
    6075576,
    6075577,
    6075578,
    5999938,
    6075579,
    6075580,
    6075582,
    6075583,
    6078345,
    6078346,
    6078347,
    6078348,
    6078349,
    6078351,
    6078429,
    6078430,
    6078431,
    6038845,
    6038841,
    6075835,
    6078336,
    6078337,
    6078338,
    6078339,
    6078340,
    6078341,
    6078342,
    6078343,
]

face_ids = [
    # "d7b3fba2-87e1-4f56-b461-06d64d4e75a0",
    # "81fbc29b-ab04-4162-ab2e-26547bd3ef12",
    # "b9c848b7-d68e-4f71-8c05-9201446348f3",
    "57d54346-a189-40e9-a37c-db3f675a41e8",
    "5e3624a7-78c8-48a0-a1b6-8c6874df50f5",
]

# for profile_id in profile_ids:
#     print(get_face_id(6059007))

with open("social_links.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["profile_id", "social_links"])

    # for profile_id, b64 in profile_responses.items():
    #     links = extract_social_links_from_grpc_response(b64)
    for profile_id in profile_ids:
        print(f"Processing profile_id {profile_id}")
        face_id = get_face_id(profile_id)
        social_links = fetch_face_profile(face_id)
        print(social_links)
        writer.writerow([profile_id, str(social_links)])


# ["https://www.instagram.com/macca03x/", "https://www.jvid.com/macca/album"]
# ["https://www.instagram.com/y.miranic/"]
# ["https://www.instagram.com/yasuyon4/"]
# ["https://www.instagram.com/yasuyon4/"]
