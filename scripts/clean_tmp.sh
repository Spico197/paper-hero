find /tmp -maxdepth 1 -type f -mmin +10 -type f -regextype posix-extended -regex '\/tmp\/arxiv\.cache\..*?\.xml' -delete
find /tmp -maxdepth 1 -type f -mmin +10 -type f -regextype posix-extended -regex '\/tmp\/dblp\.cache\..*?\.json' -delete
find /tmp -maxdepth 1 -type f -mmin +10 -type f -regextype posix-extended -regex '\/tmp\/(aclanthology|arxiv|dblp)\.(search|download)\..*?\.json' -delete
