function [raiz, iteraciones] = punto_fijo(g, x0, tol, max_iter)
% PUNTO_FIJO Método de Punto Fijo para encontrar raíces
%
% Sintaxis: [raiz, iteraciones] = punto_fijo(g, x0, tol, max_iter)
%
% Parámetros:
%   g        - Handle de la función de iteración g(x)
%   x0       - Aproximación inicial
%   tol      - Tolerancia (opcional, default: 1e-6)
%   max_iter - Máximo de iteraciones (opcional, default: 100)
%
% Retorna:
%   raiz        - Aproximación de la raíz
%   iteraciones - Matriz con historial [n, x, g(x), error]

    % Valores por defecto
    if nargin < 3, tol = 1e-6; end
    if nargin < 4, max_iter = 100; end

    % Inicialización
    x = x0;
    iteraciones = zeros(max_iter, 4);

    for i = 1:max_iter
        x_nuevo = g(x);
        error = abs(x_nuevo - x);

        % Guardar iteración
        iteraciones(i, :) = [i, x, x_nuevo, error];

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
% g = @(x) (x + 2/x) / 2;
% [raiz, hist] = punto_fijo(g, 1.0);
% fprintf('Raíz encontrada: %.10f\n', raiz);