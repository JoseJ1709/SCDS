function [coef, xi_nodos] = trazadores_cubicos_naturales(xi, yi)
% TRAZADORES_CUBICOS_NATURALES Spline cúbico natural
%
% Sintaxis: [coef, xi_nodos] = trazadores_cubicos_naturales(xi, yi)
%
% Parámetros:
%   xi - Vector de puntos x
%   yi - Vector de valores y
%
% Retorna:
%   coef - Matriz (n-1) x 4 con coeficientes [a, b, c, d]
%   xi_nodos - Puntos de los nodos

    n = length(xi);
    h = diff(xi);  % Diferencias h[i] = xi[i+1] - xi[i]

    % Sistema tridiagonal A*c = b
    A = zeros(n, n);
    b = zeros(n, 1);

    % Condiciones naturales
    A(1, 1) = 1;
    A(n, n) = 1;
    b(1) = 0;
    b(n) = 0;

    % Ecuaciones internas
    for i = 2:(n-1)
        A(i, i-1) = h(i-1);
        A(i, i) = 2*(h(i-1) + h(i));
        A(i, i+1) = h(i);
        b(i) = 3*((yi(i+1) - yi(i))/h(i) - (yi(i) - yi(i-1))/h(i-1));
    end

    % Resolver sistema
    c = A \ b;

    % Calcular otros coeficientes
    a = yi(1:end-1);
    b_coef = zeros(n-1, 1);
    d = zeros(n-1, 1);

    for i = 1:(n-1)
        b_coef(i) = (yi(i+1) - yi(i))/h(i) - h(i)*(2*c(i) + c(i+1))/3;
        d(i) = (c(i+1) - c(i))/(3*h(i));
    end

    c = c(1:end-1);

    % Matriz de coeficientes
    coef = [a, b_coef, c, d];
    xi_nodos = xi;
end


function [coef, xi_nodos] = trazadores_cubicos_sujetos(xi, yi, dy0, dyn)
% TRAZADORES_CUBICOS_SUJETOS Spline cúbico con derivadas en extremos
%
% Parámetros adicionales:
%   dy0 - Derivada en x0
%   dyn - Derivada en xn

    n = length(xi);
    h = diff(xi);

    % Sistema tridiagonal
    A = zeros(n, n);
    b = zeros(n, 1);

    % Condiciones sujetas
    A(1, 1) = 2*h(1);
    A(1, 2) = h(1);
    b(1) = 3*((yi(2) - yi(1))/h(1) - dy0);

    A(n, n-1) = h(n-1);
    A(n, n) = 2*h(n-1);
    b(n) = 3*(dyn - (yi(n) - yi(n-1))/h(n-1));

    % Ecuaciones internas
    for i = 2:(n-1)
        A(i, i-1) = h(i-1);
        A(i, i) = 2*(h(i-1) + h(i));
        A(i, i+1) = h(i);
        b(i) = 3*((yi(i+1) - yi(i))/h(i) - (yi(i) - yi(i-1))/h(i-1));
    end

    % Resolver
    c = A \ b;

    % Calcular otros coeficientes
    a = yi(1:end-1);
    b_coef = zeros(n-1, 1);
    d = zeros(n-1, 1);

    for i = 1:(n-1)
        b_coef(i) = (yi(i+1) - yi(i))/h(i) - h(i)*(2*c(i) + c(i+1))/3;
        d(i) = (c(i+1) - c(i))/(3*h(i));
    end

    c = c(1:end-1);

    coef = [a, b_coef, c, d];
    xi_nodos = xi;
end


function y = evaluar_spline(xi, coef, x)
% EVALUAR_SPLINE Evalúa el spline en x
%
% S_i(x) = a + b(x-xi) + c(x-xi)^2 + d(x-xi)^3

    y = zeros(size(x));

    for k = 1:length(x)
        x_val = x(k);

        % Encontrar intervalo
        if x_val <= xi(1)
            i = 1;
        elseif x_val >= xi(end)
            i = length(xi) - 1;
        else
            i = find(xi <= x_val, 1, 'last');
            i = min(i, size(coef, 1));
        end

        % Evaluar
        dx = x_val - xi(i);
        a = coef(i, 1);
        b = coef(i, 2);
        c = coef(i, 3);
        d = coef(i, 4);

        y(k) = a + b*dx + c*dx^2 + d*dx^3;
    end
end


function dy = derivada_spline(xi, coef, x)
% DERIVADA_SPLINE Primera derivada del spline
% S'(x) = b + 2c(x-xi) + 3d(x-xi)^2

    dy = zeros(size(x));

    for k = 1:length(x)
        x_val = x(k);

        if x_val <= xi(1)
            i = 1;
        elseif x_val >= xi(end)
            i = length(xi) - 1;
        else
            i = find(xi <= x_val, 1, 'last');
            i = min(i, size(coef, 1));
        end

        dx = x_val - xi(i);
        b = coef(i, 2);
        c = coef(i, 3);
        d = coef(i, 4);

        dy(k) = b + 2*c*dx + 3*d*dx^2;
    end
end


function ddy = segunda_derivada_spline(xi, coef, x)
% SEGUNDA_DERIVADA_SPLINE Segunda derivada del spline
% S''(x) = 2c + 6d(x-xi)

    ddy = zeros(size(x));

    for k = 1:length(x)
        x_val = x(k);

        if x_val <= xi(1)
            i = 1;
        elseif x_val >= xi(end)
            i = length(xi) - 1;
        else
            i = find(xi <= x_val, 1, 'last');
            i = min(i, size(coef, 1));
        end

        dx = x_val - xi(i);
        c = coef(i, 3);
        d = coef(i, 4);

        ddy(k) = 2*c + 6*d*dx;
    end
end


function mostrar_coeficientes_spline(xi, coef)
% Muestra los coeficientes del spline
    fprintf('\nCoeficientes de los Trazadores Cúbicos:\n');
    fprintf('========================================\n');
    fprintf('Segmento    Intervalo         a           b           c           d\n');
    fprintf('------------------------------------------------------------------------\n');

    for i = 1:size(coef, 1)
        fprintf('S_%d(x)     [%.2f, %.2f]   %10.6f  %10.6f  %10.6f  %10.6f\n', ...
                i-1, xi(i), xi(i+1), coef(i,1), coef(i,2), coef(i,3), coef(i,4));
    end

    fprintf('========================================\n\n');

    fprintf('Ecuaciones:\n');
    for i = 1:size(coef, 1)
        fprintf('S_%d(x) = %.6f %+.6f(x-%.2f) %+.6f(x-%.2f)² %+.6f(x-%.2f)³\n', ...
                i-1, coef(i,1), coef(i,2), xi(i), coef(i,3), xi(i), coef(i,4), xi(i));
    end
end


% ========================================================================
% SCRIPT DE EJEMPLO
% ========================================================================

% Ejemplo 1: Trazadores naturales
fprintf('========================================\n');
fprintf('TRAZADORES CÚBICOS NATURALES\n');
fprintf('========================================\n\n');

xi = [0, 1, 2, 3, 4];
yi = [0, 0.5, 2.0, 1.5, 1.0];

fprintf('Puntos dados:\n');
for i = 1:length(xi)
    fprintf('  (%.1f, %.1f)\n', xi(i), yi(i));
end

[coef, xi_nodos] = trazadores_cubicos_naturales(xi, yi);
mostrar_coeficientes_spline(xi, coef);

% Verificar condiciones naturales
fprintf('\nVerificación condiciones naturales:\n');
fprintf('  S"(%.1f) = %.6f (debe ser ≈0)\n', xi(1), segunda_derivada_spline(xi, coef, xi(1)));
fprintf('  S"(%.1f) = %.6f (debe ser ≈0)\n', xi(end), segunda_derivada_spline(xi, coef, xi(end)));

% Graficar
x_plot = linspace(xi(1), xi(end), 500);
y_plot = evaluar_spline(xi, coef, x_plot);
dy_plot = derivada_spline(xi, coef, x_plot);
ddy_plot = segunda_derivada_spline(xi, coef, x_plot);

figure('Position', [100, 100, 1000, 800]);

subplot(3,1,1);
plot(x_plot, y_plot, 'b-', 'LineWidth', 2); hold on;
plot(xi, yi, 'ro', 'MarkerSize', 10, 'MarkerFaceColor', 'r');
grid on;
ylabel('S(x)', 'FontSize', 12);
title('Trazadores Cúbicos Naturales', 'FontSize', 14, 'FontWeight', 'bold');
legend('S(x)', 'Puntos dados');

subplot(3,1,2);
plot(x_plot, dy_plot, 'g-', 'LineWidth', 2);
yline(0, 'k--', 'Alpha', 0.3);
grid on;
ylabel('S''(x)', 'FontSize', 12);
legend('S''(x)');

subplot(3,1,3);
plot(x_plot, ddy_plot, 'r-', 'LineWidth', 2);
yline(0, 'k--', 'Alpha', 0.3);
grid on;
xlabel('x', 'FontSize', 12);
ylabel('S''''(x)', 'FontSize', 12);
legend('S''''(x)');

fprintf('\n✅ Gráfica generada\n');