function [raiz, iteraciones] = steffensen(g, x0, tol, max_iter)
% STEFFENSEN Método de Steffensen para encontrar raíces
%
% Sintaxis: [raiz, iteraciones] = steffensen(g, x0, tol, max_iter)
%
% Parámetros:
%   g        - Handle de la función de punto fijo
%   x0       - Aproximación inicial
%   tol      - Tolerancia (opcional, default: 1e-6)
%   max_iter - Máximo de iteraciones (opcional, default: 100)
%
% Retorna:
%   raiz        - Aproximación de la raíz
%   iteraciones - Matriz con historial

    % Valores por defecto
    if nargin < 3, tol = 1e-6; end
    if nargin < 4, max_iter = 100; end

    % Inicialización
    x = x0;
    iteraciones = zeros(max_iter, 6);

    for i = 1:max_iter
        gx = g(x);
        ggx = g(gx);

        % Calcular denominador
        denominador = ggx - 2*gx + x;

        % Verificar división por cero
        if abs(denominador) < 1e-10
            fprintf('Advertencia: División por cero en iteración %d\n', i);
            x_nuevo = gx;  % Usar punto fijo simple
        else
            % Fórmula de Steffensen
            x_nuevo = x - (gx - x)^2 / denominador;
        end

        error = abs(x_nuevo - x);

        % Guardar iteración
        iteraciones(i, :) = [i, x, gx, ggx, x_nuevo, error];

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
% [raiz, hist] = steffensen(g, 1.0);
% fprintf('Raíz encontrada: %.10f\n', raiz);