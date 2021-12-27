#!/usr/bin/python3


import requests
from queue import Queue
from concurrent.futures import ThreadPoolExecutor
import optparse


class bypass:

    def __init__(self, url):
        self.url = url
        self.result = {}

    def post(self):
        data = requests.post(self.url, headers={"Content-length": '0'})
        return data.status_code, len(data.content)

    def get(self):
        data = requests.get(self.url)

        return data.status_code, len(data.content)

    def put(self):
        data = requests.put(self.url)

        return (data.status_code, len(data.content))

    def head(self):
        data = requests.head(self.url)

        return (data.status_code, len(data.content))

    def delete(self):
        data = requests.delete(self.url)

        return (data.status_code, len(data.content))

    def patch(self):
        data = requests.patch(self.url)

        return (data.status_code, len(data.content))

    def option(self):
        data = requests.options(self.url)

        return (data.status_code, len(data.content))

    def trace(self):
        data = requests.Request('TRACE', self.trace)

        return (data.status_code, len(data.content))

    def req(self):
        self.result['GET'] = self.get()
        self.result["POST"] = self.post()
        self.result["PUT"] = self.put()
        self.result["PATCH"] = self.patch()
        self.result["OPTIONS"] = self.option()
        #    self.result["TRACE"] = self.trace()
        self.result["DELETE"] = self.delete()
        self.result["HEAD"] = self.head()


queue = Queue()


def pool(filename, threads, out):
    print("file_name=\033[33m{}\033[0m    threads=\033[33m{}\033[0m        ".format(filename, threads))
    Lines = open(filename, 'r').readlines()
    with ThreadPoolExecutor(max_workers=threads) as executor:
        for i in Lines:
            url = i.replace("\n", "")
            executor.submit(single_url, url)
    done(out)


def single_url(url):
    b = bypass(url)
    # print(b.url)
    b.req()
    queue.put(b)


def done(out):
    a = []
    while not queue.empty():
        obj = queue.get()
        print("URL: {}".format(obj.url))
        a.append(obj)
        with open(out, 'a') as out_file:
            for key, value in obj.result.items():
                if value[0] == 200:
                    print("{} request: \033[32m{}   {}\033[0m".format(key, value[0], value[1]))
                    out_file.write("{} request: \033[32m{}   {}\033[0m".format(key, value[0], value[1]))
                else:
                    print("{} request: \033[31m{}  {}\033[0m".format(key, value[0], value[1]))
                    out_file.write("{} request: \033[31m{}  {}\033[0m".format(key, value[0], value[1]))
            out_file.write("\n")
            print("\n")

def logo():
    print(
        """
            \033[32m
                           __  __    __                               
           ____ ___  ___  / /_/ /_  / /_  __  ______  ____ ___________
          / __ `__ \/ _ \/ __/ __ \/ __ \/ / / / __ \/ __ `/ ___/ ___/
         / / / / / /  __/ /_/ / / / /_/ / /_/ / /_/ / /_/ (__  |__  ) 
        /_/ /_/ /_/\___/\__/_/ /_/_.___/\__, / .___/\__,_/____/____/
          github.com/medbsq/methBypass /____/_/  by MedBsq
                                                                       
            \033[0m
        """

    )


def Main():
    parser = optparse.OptionParser("help:\n" + \
                                   "methby.py -u <url> -t <threads> -o <output_file>\n" + \
                                   "methby.py -f <urls list> -t <threads> -o <output_file>")
    parser.add_option("-f", dest="url_file", type="string", help="spicify urls file")
    parser.add_option("-u", dest="url", type="string", help="spicify url ")
    parser.add_option("-t", dest="threads", type="int", help="spicify nybmer of threads")
    parser.add_option("-o", dest="output", type="string", help="spicify output file")

    (options, args) = parser.parse_args()
    threads = 20
    out = "/tmp/out.txt"

    if (options.threads != None):
        threads = options.threads
    if (options.output != None):
        out = options.output

    if (options.url_file != None):
        file = options.url_file
        pool(file, threads, out)
        exit(0)

    elif (options.url != None):
        url = options.url
        single_url(url)
        done(out)

        exit(0)

    else:
        print(parser.usage)
        exit(1)


if __name__ == '__main__':
    logo()
    Main()
