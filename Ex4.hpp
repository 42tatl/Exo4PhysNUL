// PhysicsUtils.hpp
#ifndef EX4_HPP
#define EX4_HPP

// Constants
const double PI = 3.14159265358979323846;
const double epsilon_0 = 8.854187817e-12;

// Function declarations
double epsilon(bool uniform_rho_case, double r, double r1, double R,
               double epsilon_a, double epsilon_b);

double rho_epsilon(bool uniform_rho_case, double r, double rho0, double r1);

#endif // EX4_HPP
