
function [raiz, iteraciones] = newton(f, df, x0, tol, max_iter)
% NEWTON Método de Newton-Raphson para encontrar raíces
%
% Sintaxis: [raiz, iteraciones] = newton(f, df, x0, tol, max_iter)
%
% Parámetros:
%   f        - Handle de la función
%   df       - Handle de la derivada
%   x0       - Aproximación inicial
%   tol      - Tolerancia (opcional, default: 1e-6)
%   max_iter - Máximo de iteraciones (opcional, default: 100)
%
% Retorna:
%   raiz        - Aproximación de la raíz
%   iteraciones - Matriz con historial [n, x, f(x), f'(x), x_nuevo, error]

    % Valores por defecto
    if nargin < 4, tol = 1e-6; end
    if nargin < 5, max_iter = 100; end

    % Inicialización
    x = x0;
    iteraciones = zeros(max_iter, 6);

    for i = 1:max_iter
        fx = f(x);
        dfx = df(x);

        % Verificar división por cero
        if abs(dfx) < 1e-10
            fprintf('Error: Derivada muy pequeña en iteración %d\n', i);
            raiz = NaN;
            iteraciones = iteraciones(1:i-1, :);
            return;
        end

        x_nuevo = x - fx / dfx;
        error = abs(x_nuevo - x);

        % Guardar iteración
        iteraciones(i, :) = [i, x, fx, dfx, x_nuevo, error];

        % Criterio de convergencia
        if error < tol
            fprintf('Convergencia alcanzada en %d iteraciones\n', i);
            raiz = x_nuevo;
            iteraciones = iteraciones(1:i, :);
            return;
        end

        x = x_nuevo;
    end

    fprintf('No se alcanzó convergencia en %d iteraciones\n', max_iter);
    raiz = x;
    iteraciones = iteraciones(1:max_iter, :);
end

% Ejemplo de uso:
% f = @(x) x^2 - 2;
% df = @(x) 2*x;
% [raiz, hist] = newton(f, df, 1.0);
% fprintf('Raíz encontrada: %.10f\n', raiz);