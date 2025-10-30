function [Px, tabla] = diferencias_divididas(xi, yi, x)
% DIFERENCIAS_DIVIDIDAS Interpolación por diferencias divididas de Newton
%
% Sintaxis: [Px, tabla] = diferencias_divididas(xi, yi, x)
%
% Parámetros:
%   xi - Vector de puntos x conocidos
%   yi - Vector de valores y conocidos
%   x  - Punto(s) donde interpolar
%
% Retorna:
%   Px    - Valor del polinomio en x
%   tabla - Tabla de diferencias divididas

    n = length(xi);

    % Crear tabla de diferencias divididas
    tabla = zeros(n, n);
    tabla(:, 1) = yi';  % Primera columna

    % Calcular diferencias divididas
    for j = 2:n
        for i = 1:(n-j+1)
            tabla(i, j) = (tabla(i+1, j-1) - tabla(i, j-1)) / ...
                         (xi(i+j-1) - xi(i));
        end
    end

    % Evaluar polinomio de Newton
    Px = tabla(1, 1) * ones(size(x));
    producto = ones(size(x));

    for i = 2:n
        producto = producto .* (x - xi(i-1));
        Px = Px + tabla(1, i) * producto;
    end
end


function mostrar_tabla_diferencias(xi, yi, tabla)
% Muestra la tabla de diferencias divididas
    n = length(xi);

    fprintf('\nTabla de Diferencias Divididas:\n');
    fprintf('=====================================\n');
    fprintf('%5s %10s %15s', 'i', 'xi', 'f[xi]');

    for j = 2:n
        fprintf(' %15s', sprintf('f[...]_{%d}', j));
    end
    fprintf('\n');
    fprintf('-------------------------------------\n');

    for i = 1:n
        fprintf('%5d %10.4f ', i-1, xi(i));
        for j = 1:n
            if j <= (n - i + 1) && (tabla(i, j) ~= 0 || j == 1)
                fprintf('%15.6f ', tabla(i, j));
            else
                fprintf('%15s ', '');
            end
        end
        fprintf('\n');
    end

    fprintf('=====================================\n');

    % Mostrar coeficientes
    fprintf('\nCoeficientes del polinomio de Newton:\n');
    for i = 1:n
        fprintf('a%d = %.6f\n', i-1, tabla(1, i));
    end
end


% ========================================================================
% SCRIPT DE EJEMPLO
% ========================================================================

xi = [1.0, 1.3, 1.6, 1.9, 2.2];
yi = [0.7651977, 0.6200860, 0.4554022, 0.2818186, 0.1103623];

fprintf('========================================\n');
fprintf('DIFERENCIAS DIVIDIDAS (NEWTON)\n');
fprintf('========================================\n\n');

fprintf('Puntos dados:\n');
for i = 1:length(xi)
    fprintf('  (%.1f, %.7f)\n', xi(i), yi(i));
end

% Calcular tabla
[~, tabla] = diferencias_divididas(xi, yi, 0);
mostrar_tabla_diferencias(xi, yi, tabla);

% Evaluar en un punto
x_test = 1.5;
Px_test = diferencias_divididas(xi, yi, x_test);
fprintf('\nInterpolación en x = %.1f:\n', x_test);
fprintf('  P(%.1f) = %.7f\n', x_test, Px_test);

% Graficar
x_plot = linspace(min(xi)-0.2, max(xi)+0.2, 500);
y_plot = diferencias_divididas(xi, yi, x_plot);

figure('Position', [100, 100, 800, 600]);
plot(x_plot, y_plot, 'b-', 'LineWidth', 2); hold on;
plot(xi, yi, 'ro', 'MarkerSize', 10, 'MarkerFaceColor', 'r');
grid on;
xlabel('x', 'FontSize', 12);
ylabel('y', 'FontSize', 12);
title('Interpolación por Diferencias Divididas', 'FontSize', 14);
legend('Polinomio de Newton', 'Puntos dados');

fprintf('\n✅ Gráfica generada\n');