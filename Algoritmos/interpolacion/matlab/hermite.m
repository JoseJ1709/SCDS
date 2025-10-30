function [Px, z, tabla] = hermite(xi, yi, dyi, x)
% HERMITE Interpolación de Hermite con diferencias divididas
%
% Sintaxis: [Px, z, tabla] = hermite(xi, yi, dyi, x)
%
% Parámetros:
%   xi  - Vector de puntos x conocidos
%   yi  - Vector de valores y conocidos
%   dyi - Vector de derivadas dy/dx conocidas
%   x   - Punto(s) donde interpolar
%
% Retorna:
%   Px    - Valor del polinomio en x
%   z     - Puntos duplicados (xi repetidos)
%   tabla - Tabla de diferencias divididas

    n = length(xi);
    m = 2 * n;  % Puntos duplicados

    % Crear array z con puntos duplicados
    z = zeros(1, m);
    z(1:2:m) = xi;  % Índices impares
    z(2:2:m) = xi;  % Índices pares

    % Tabla de diferencias divididas
    tabla = zeros(m, m);

    % Primera columna: valores f(xi) duplicados
    tabla(1:2:m, 1) = yi;
    tabla(2:2:m, 1) = yi;

    % Segunda columna: derivadas y diferencias
    % En puntos duplicados: usar derivadas
    tabla(1:2:m-1, 2) = dyi;

    % Entre puntos distintos: fórmula normal
    for i = 2:2:m-1
        tabla(i, 2) = (tabla(i+1, 1) - tabla(i, 1)) / (z(i+1) - z(i));
    end

    % Resto de columnas: diferencias divididas normales
    for j = 3:m
        for i = 1:m-j+1
            tabla(i, j) = (tabla(i+1, j-1) - tabla(i, j-1)) / ...
                         (z(i+j-1) - z(i));
        end
    end

    % Evaluar polinomio de Newton con puntos z
    Px = tabla(1, 1) * ones(size(x));
    producto = ones(size(x));

    for i = 2:m
        producto = producto .* (x - z(i-1));
        Px = Px + tabla(1, i) * producto;
    end
end


function mostrar_tabla_hermite(xi, yi, dyi, z, tabla)
% Muestra la tabla de diferencias divididas de Hermite
    n = length(xi);
    m = 2 * n;

    fprintf('\nTabla de Diferencias Divididas de Hermite:\n');
    fprintf('================================================================\n');
    fprintf('%5s %10s %15s %20s %25s\n', 'i', 'z[i]', 'f[z[i]]', ...
            'f[z[i],z[i+1]]', 'f[z[i],...,z[i+2]]');
    fprintf('----------------------------------------------------------------\n');

    for i = 1:m
        fprintf('%5d %10.4f %15.6f ', i-1, z(i), tabla(i, 1));

        if i < m
            fprintf('%20.6f ', tabla(i, 2));
        else
            fprintf('%20s ', '');
        end

        if i < m-1
            fprintf('%25.6f', tabla(i, 3));
        end

        fprintf('\n');
    end

    fprintf('================================================================\n');
    fprintf('\nPuntos originales: %d\n', n);
    fprintf('Puntos en tabla z (duplicados): %d\n', m);
    fprintf('Grado del polinomio: %d\n', m-1);
end


% ========================================================================
% SCRIPT DE EJEMPLO 1
% ========================================================================

fprintf('========================================\n');
fprintf('INTERPOLACIÓN DE HERMITE\n');
fprintf('========================================\n\n');

% Datos de ejemplo
xi = [1.3, 1.6, 1.9];
yi = [0.6200860, 0.4554022, 0.2818186];
dyi = [-0.5220232, -0.5698959, -0.5811571];  % Derivadas

fprintf('Datos dados:\n');
fprintf('%-10s %-15s %-15s\n', 'x', 'y = f(x)', 'y'' = f''(x)');
fprintf('--------------------------------------------\n');
for i = 1:length(xi)
    fprintf('%-10.1f %-15.7f %-15.7f\n', xi(i), yi(i), dyi(i));
end

% Calcular tabla
[~, z, tabla] = hermite(xi, yi, dyi, 0);
mostrar_tabla_hermite(xi, yi, dyi, z, tabla);

% Evaluar en un punto
x_test = 1.5;
Px_test = hermite(xi, yi, dyi, x_test);
fprintf('\nInterpolación en x = %.1f:\n', x_test);
fprintf('  P(%.1f) = %.7f\n', x_test, Px_test);

% Comparar con Newton simple (sin derivadas)
% Nota: Necesitarías tener diferencias_divididas.m
% fprintf('  Newton simple: %.7f\n', newton(xi, yi, x_test));

% Graficar
x_plot = linspace(min(xi)-0.2, max(xi)+0.2, 500);
y_hermite = hermite(xi, yi, dyi, x_plot);

% También calcular Newton para comparación (si está disponible)
% y_newton = diferencias_divididas(xi, yi, x_plot);

figure('Position', [100, 100, 1000, 600]);
plot(x_plot, y_hermite, 'b-', 'LineWidth', 2); hold on;
plot(xi, yi, 'ro', 'MarkerSize', 10, 'MarkerFaceColor', 'r');

% Dibujar tangentes (derivadas)
for i = 1:length(xi)
    x_tang = [xi(i)-0.1, xi(i)+0.1];
    y_tang = yi(i) + dyi(i) * (x_tang - xi(i));
    plot(x_tang, y_tang, 'r--', 'LineWidth', 1, 'Color', [1 0 0 0.5]);
end

grid on;
xlabel('x', 'FontSize', 12);
ylabel('y', 'FontSize', 12);
title('Interpolación de Hermite', 'FontSize', 14, 'FontWeight', 'bold');
legend('Hermite (con derivadas)', 'Puntos dados', 'Tangentes (derivadas)');

fprintf('\n✅ Gráfica generada\n');