function coef = interpolacion_cubica_fija(xi, yi)
% INTERPOLACION_CUBICA_FIJA Polinomio cúbico para 4 puntos
%
% Sintaxis: coef = interpolacion_cubica_fija(xi, yi)
%
% Parámetros:
%   xi - Vector de 4 puntos x
%   yi - Vector de 4 valores y
%
% Retorna:
%   coef - Vector [a0, a1, a2, a3] con coeficientes

    if length(xi) ~= 4 || length(yi) ~= 4
        error('Se requieren exactamente 4 puntos');
    end

    % Matriz de Vandermonde
    V = [ones(4,1), xi(:), xi(:).^2, xi(:).^3];

    % Resolver sistema V * coef = yi
    coef = V \ yi(:);
end


function y = evaluar_cubica(coef, x)
% Evalúa el polinomio cúbico
% P(x) = a0 + a1*x + a2*x^2 + a3*x^3
    y = coef(1) + coef(2)*x + coef(3)*x.^2 + coef(4)*x.^3;
end


function dy = derivada_cubica(coef, x)
% Primera derivada
% P'(x) = a1 + 2*a2*x + 3*a3*x^2
    dy = coef(2) + 2*coef(3)*x + 3*coef(4)*x.^2;
end


function ddy = segunda_derivada_cubica(coef, x)
% Segunda derivada
% P''(x) = 2*a2 + 6*a3*x
    ddy = 2*coef(3) + 6*coef(4)*x;
end


% ========================================================================
% SCRIPT DE EJEMPLO
% ========================================================================

fprintf('========================================\n');
fprintf('INTERPOLACIÓN CÚBICA FIJA (4 PUNTOS)\n');
fprintf('========================================\n\n');

xi = [0, 1, 2, 3];
yi = [1, 2, 0, 4];

fprintf('Puntos dados:\n');
for i = 1:4
    fprintf('  (%g, %g)\n', xi(i), yi(i));
end

% Calcular coeficientes
coef = interpolacion_cubica_fija(xi, yi);

fprintf('\nPolinomio cúbico:\n');
fprintf('P(x) = %.6f %+.6fx %+.6fx² %+.6fx³\n', coef(1), coef(2), coef(3), coef(4));

% Verificar
fprintf('\nVerificación:\n');
for i = 1:4
    p_x = evaluar_cubica(coef, xi(i));
    fprintf('  P(%g) = %.6f (debe ser %g)\n', xi(i), p_x, yi(i));
end

% Evaluar en punto intermedio
x_test = 1.5;
y_test = evaluar_cubica(coef, x_test);
dy_test = derivada_cubica(coef, x_test);
ddy_test = segunda_derivada_cubica(coef, x_test);

fprintf('\nEvaluación en x = %.1f:\n', x_test);
fprintf('  P(%.1f) = %.6f\n', x_test, y_test);
fprintf('  P''(%.1f) = %.6f\n', x_test, dy_test);
fprintf('  P''''(%.1f) = %.6f\n', x_test, ddy_test);

% Graficar
x_plot = linspace(min(xi)-0.5, max(xi)+0.5, 500);
y_plot = evaluar_cubica(coef, x_plot);

figure('Position', [100, 100, 800, 600]);
plot(x_plot, y_plot, 'b-', 'LineWidth', 2); hold on;
plot(xi, yi, 'ro', 'MarkerSize', 10, 'MarkerFaceColor', 'r');
grid on;
xlabel('x', 'FontSize', 12);
ylabel('y', 'FontSize', 12);
title('Interpolación Cúbica (4 puntos)', 'FontSize', 14, 'FontWeight', 'bold');
legend('Polinomio cúbico', 'Puntos dados');

for i = 1:4
    text(xi(i), yi(i), sprintf('  (%.1f, %.1f)', xi(i), yi(i)), 'FontSize', 10);
end

fprintf('\n✅ Gráfica generada\n');