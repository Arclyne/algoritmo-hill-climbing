"""Hill-Climbing para la función Sphere (Algoritmos 1 y 4 del material de Metaheurísticas)."""

import random
from dataclasses import dataclass

LOWER_BOUND = -10.0
UPPER_BOUND = 10.0

DIMENSIONS = 2

ALTERATION_PROBABILITY = 0.5

STEP_SIZE = 1.0

MAX_EVALUATIONS = 10_000

SEED = 42


@dataclass
class HillClimbingResult:
    """Lo que regresa el algoritmo al terminar."""
    initial_solution: list
    initial_quality: float
    best_solution: list
    best_quality: float
    iterations: int
    evaluations: int
    accepted: int


def validate_parameters(dimensions, alteration_probability, step_size, max_evaluations):
    if dimensions < 1:
        raise ValueError(f"dimensions must be at least 1, got {dimensions}")
    if not 0 < alteration_probability <= 1:
        raise ValueError(f"alteration_probability must be in (0, 1], got {alteration_probability}")
    if step_size <= 0:
        raise ValueError(f"step_size must be greater than 0, got {step_size}")
    if max_evaluations < 1:
        raise ValueError(f"max_evaluations must be at least 1, got {max_evaluations}")


def sphere(x):
    total = 0.0
    for value in x:
        total += value ** 2
    return total


def random_solution(dimensions, lower_bound, upper_bound, rng):
    return [rng.uniform(lower_bound, upper_bound) for _ in range(dimensions)]


def bounded_uniform_convolution(x, alteration_probability, step_size, lower_bound, upper_bound, rng):
    neighbor = x.copy()

    for i in range(len(neighbor)):
        if alteration_probability >= rng.random():

            while True:
                noise = rng.uniform(-step_size, step_size)
                if lower_bound <= neighbor[i] + noise <= upper_bound:
                    break
            neighbor[i] += noise

    return neighbor


def hill_climbing(dimensions, alteration_probability, step_size, max_evaluations,
                  lower_bound, upper_bound, rng):
    
    current = random_solution(dimensions, lower_bound, upper_bound, rng)
    current_quality = sphere(current)
    evaluations = 1

    initial_solution = current.copy()
    initial_quality = current_quality
    iterations = 0
    accepted = 0

    while evaluations < max_evaluations:
        candidate = bounded_uniform_convolution(
            current, alteration_probability, step_size, lower_bound, upper_bound, rng
        )
        candidate_quality = sphere(candidate)
        evaluations += 1
        iterations += 1

        if candidate_quality < current_quality:
            current = candidate
            current_quality = candidate_quality
            accepted += 1
       
    return HillClimbingResult(
        initial_solution=initial_solution,
        initial_quality=initial_quality,
        best_solution=current,
        best_quality=current_quality,
        iterations=iterations,
        evaluations=evaluations,
        accepted=accepted,
    )


def format_vector(x, decimals=6):
    """Muestra un vector con pocos decimales para que sea legible."""
    return "[" + ", ".join(f"{value:.{decimals}f}" for value in x) + "]"


def main():
    validate_parameters(DIMENSIONS, ALTERATION_PROBABILITY, STEP_SIZE, MAX_EVALUATIONS)

    rng = random.Random(SEED)

    print("Hill-Climbing parameters")
    print(f"  Dimensions (n):             {DIMENSIONS}")
    print(f"  Bounds:                     [{LOWER_BOUND}, {UPPER_BOUND}]")
    print(f"  Alteration probability (p): {ALTERATION_PROBABILITY}")
    print(f"  Step size (r):              {STEP_SIZE}")
    print(f"  Max evaluations:            {MAX_EVALUATIONS}")
    print(f"  Seed:                       {SEED}")

    result = hill_climbing(
        DIMENSIONS, ALTERATION_PROBABILITY, STEP_SIZE, MAX_EVALUATIONS,
        LOWER_BOUND, UPPER_BOUND, rng,
    )

    acceptance_rate = 100 * result.accepted / result.iterations if result.iterations else 0.0

    print("\nResults")
    print(f"  Initial solution: {format_vector(result.initial_solution)}")
    print(f"  Initial f(x):     {result.initial_quality:.6e}")
    print(f"  Best solution:    {format_vector(result.best_solution)}")
    print(f"  Best f(x):        {result.best_quality:.6e}")
    print(f"  Iterations:       {result.iterations}")
    print(f"  Evaluations:      {result.evaluations}")
    print(f"  Accepted moves:   {result.accepted} ({acceptance_rate:.1f}%)")


if __name__ == "__main__":
    main()
