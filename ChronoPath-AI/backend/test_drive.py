from dataset_engine.google_drive import list_files


INBOX_FOLDER_ID = "1ZkvdLJUJ0ZrdLlyrIIrUe9zR8MsyUImW"


print("\n")
print("=" * 50)
print("       CHRONOPATH AI - GOOGLE DRIVE TEST")
print("=" * 50)
print()


files = list_files(
    INBOX_FOLDER_ID
)


if not files:

    print("No files found in Inbox.")

else:

    print(
        f"Found {len(files)} file(s):\n"
    )

    for number, file in enumerate(
        files,
        start=1
    ):

        print(
            f"{number}. {file['name']}"
        )

        print(
            f"   ID: {file['id']}"
        )

        print(
            f"   Type: {file['mimeType']}"
        )

        print(
            f"   Modified: {file.get('modifiedTime', 'N/A')}"
        )

        print(
            "-" * 50
        )


print()
print("Google Drive connection successful.")