def trim_footer(fname):
    # list to store file lines
    lines = []
    # read file
    with open(fname, 'r') as fp:
    # read an store all lines into list
        lines = fp.readlines()

    # Write file
    with open(fname, 'w') as fp:
    # iterate each line
        for number, line in enumerate(lines):
        # delete line 5 and 8. or pass any Nth line you want to remove
        # note list index starts from 0
            if number not in [(len(lines) - 3), (len(lines) - 2), (len(lines) - 1)]:
                fp.write(line)

trim_footer('ufc_base_scrape_results.md')