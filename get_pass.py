import plistlib
import sys

def read_user_plist(username):
    plist_path = f"/var/db/dslocal/nodes/Default/users/{username}.plist"
    with open(plist_path, "rb") as f:
        plist = plistlib.load(f)

    return plist

def main(args):
    username = args[1]
    user_plist = read_user_plist(username)

    # Nested binary plist
    nested_bplist = user_plist["ShadowHashData"]
    shadow_hash_plist = plistlib.loads(nested_bplist[0])
    print(shadow_hash_plist)

if __name__ == "__main__":
    main(sys.argv)