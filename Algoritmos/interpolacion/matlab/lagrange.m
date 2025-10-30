function [Px, coef] = lagrange(xi, yi, x)
% LAGRANGE Interpolación de Lagrange
%
% Sintaxis: [Px, coef] = lagrange(xi, yi, x)
%
% Parámetros:
%   xi - Vector de puntos x conocidos
%   yi - Vector de valores y conocidos
%   x  - Punto(s) donde interpolar
%
% Retorna:
%   Px   - Valor del polinomio en x
%   coef - Coeficientes del polinomio

    n = length(xi);
    Px = zeros(size(x));

    % P(x) = Σ yi · Li(x)
    for i = 1:n
        Li = ones(size(x));

        % Calcular Li(x)
        for j = 1:n
            if j ~= i
                Li = Li .* (x - xi(j)) / (xi(i) - xi(j));
            end
        end

        Px = Px + yi(i) * Li;
    end

    % Calcular coeficientes (opcional)
    if nargout > 1
        coef = calcular_coeficientes(xi, yi);
    end
end


function coef = calcular_coeficientes(xi, yi)
% Calcula los coeficientes del polinomio en forma estándar
    n = length(xi);
    coef = zeros(1, n);

    for i = 1:n
        % Construir Li(x) en forma de coeficientes
        Li_coef = yi(i);

        for j = 1:n
            if j ~= i
                % Multiplicar por (x - xj)/(xi - xj)
                factor = [-xi(j), 1] / (xi(i) - xi(j));
                Li_coef = conv(Li_coef, factor);
            end
        end

        % Ajustar tamaño y sumar
        if length(Li_coef) > n
            Li_coef = Li_coef(1:n);
        elseif length(Li_coef) < n
            Li_coef = [Li_coef, zeros(1, n - length(Li_coef))];
        end

        coef = coef + Li_coef;
    end
end


function mostrar_polinomio(coef)
% Muestra el polinomio en forma legible
    fprintf('P(x) = ');
    n = length(coef);

    for i = 1:n
        if abs(coef(i)) > 1e-10
            if i == 1
                fprintf('%.6f', coef(i));
            elseif i == 2
                fprintf(' %+.6f*x', coef(i));
            else
                fprintf(' %+.6f*x^%d', coef(i), i-1);
            end
        end
    end
    fprintf('\n');
end


% ========================================================================
% SCRIPT DE EJEMPLO
% ========================================================================
% Para usar este ejemplo, guárdalo como lagrange_ejemplo.m

% Datos de ejemplo
xi = [0, 1, 2, 3];
yi = [1, 3, 2, 5];

fprintf('========================================\n');
fprintf('INTERPOLACIÓN DE LAGRANGE\n');
fprintf('========================================\n\n');

fprintf('Puntos dados:\n');
fprintf('x = '); fprintf('%g ', xi); fprintf('\n');
fprintf('y = '); fprintf('%g ', yi); fprintf('\n\n');

% Calcular interpolación
[~, coef] = lagrange(xi, yi, 0);
fprintf('Polinomio interpolante:\n');
mostrar_polinomio(coef);

% Evaluar en puntos intermedios
x_test = [0.5, 1.5, 2.5];
Px_test = lagrange(xi, yi, x_test);

fprintf('\nEvaluación en puntos intermedios:\n');
for i = 1:length(x_test)
    fprintf('  P(%.1f) = %.6f\n', x_test(i), Px_test(i));
end

% Verificación
fprintf('\nVerificación:\n');
Px_verif = lagrange(xi, yi, xi);
for i = 1:length(xi)
    fprintf('  P(%g) = %.6f  (original: %g)\n', xi(i), Px_verif(i), yi(i));
end

% Graficar
x_plot = linspace(min(xi)-0.5, max(xi)+0.5, 500);
y_plot = lagrange(xi, yi, x_plot);

figure('Position', [100, 100, 800, 600]);
plot(x_plot, y_plot, 'b-', 'LineWidth', 2); hold on;
plot(xi, yi, 'ro', 'MarkerSize', 10, 'MarkerFaceColor', 'r');
grid on;
xlabel('x', 'FontSize', 12);
ylabel('y', 'FontSize', 12);
title('Interpolación de Lagrange', 'FontSize', 14, 'FontWeight', 'bold');
legend('Polinomio interpolante', 'Puntos dados');

% Anotar puntos
for i = 1:length(xi)
    text(xi(i), yi(i), sprintf('  (%.1f, %.1f)', xi(i), yi(i)), ...
         'FontSize', 10);
end

fprintf('\n✅ Gráfica generada\n');