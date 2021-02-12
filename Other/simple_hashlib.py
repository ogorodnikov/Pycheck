from hashlib import md5, sha224, sha256, sha384, sha512, sha1

HASH_FUNCTIONS = {'md5': md5,
                  'sha1': sha1,
                  'sha224': sha224,
                  'sha256': sha256,
                  'sha384': sha384,
                  'sha512': sha512}


def checkio(hashed_string, algorithm):
    print('Hashed string:', hashed_string)
    print('Algorithm:', algorithm)

    hash_function = HASH_FUNCTIONS[algorithm]
    result_hash = hash_function(hashed_string.encode()).hexdigest()

    print('Result hash:', result_hash)
    print()
    return result_hash


if __name__ == '__main__':
    assert checkio('welcome', 'md5') == '40be4e59b9a2a2b5dffb918c0e86b3d7'
    assert checkio('happy spam', 'sha224') == '6e9dc3e01d57f1598c2b40ce59fc3527e698c77b15d0840ae96a8b5e'
    assert checkio('welcome to pycon', 'sha256')
