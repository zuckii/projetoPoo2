def gen_particles(count):
    import random
    rng = random.Random(count)
    particles = []
    for i in range(count):
        particles.append((
            round(rng.uniform(3.0, 8.0), 6),
            rng.randint(50, 255),
            rng.randint(50, 255),
            rng.randint(150, 255),
            round(rng.uniform(1, 4), 6)
        ))
    return particles


def main():
    a = gen_particles(2000)
    b = gen_particles(2000)
    print('igual?', a == b)
    # print a few samples
    for i in range(3):
        print(a[i])

if __name__ == '__main__':
    main()
