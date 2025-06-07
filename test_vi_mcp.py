from vi_mcp import (
    get_cve_details_with_history,
)


async def main():
    cve_id = "CVE-2023-35078"  # Updated test CVE ID
    result = await get_cve_details_with_history(cve_id)
    print(result)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
