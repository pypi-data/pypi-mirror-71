# neural-texturize — Copyright (c) 2020, Novelty Factory KG.  See LICENSE for details.

import torch.optim


class SolverLBFGS:
    """Encapsulate the L-BFGS optimizer from PyTorch with a standard interface.
    """

    def __init__(self, objective, image, lr=1.0):
        self.objective = objective
        self.image = image
        self.lr = lr
        self.optimizer = torch.optim.LBFGS(
            [image], lr=lr, max_iter=2, max_eval=4, history_size=10
        )
        self.iteration = 1

    def step(self):
        # The first 20 iterations, we increase the learning rate slowly to full value.
        for group in self.optimizer.param_groups:
            group["lr"] = self.lr * min(self.iteration / 20.0, 1.0) ** 2

        # Each iteration we reset the accumulated gradients and compute the objective.
        loss, scores = None, None
        def _wrap():
            nonlocal loss, scores
            self.iteration += 1
            self.image.data.clamp_(0.0, 1.0)

            self.optimizer.zero_grad()
            loss, scores = self.objective(self.image)

            self.image.grad.data.clamp_(-1e-1, +1e-1)
            return loss

        # This optimizer decides when and how to call the objective.
        self.optimizer.step(_wrap)
        return loss, scores


class SolverSGD:
    """Encapsulate the SGD or Adam optimizers from PyTorch with a standard interface.
    """

    def __init__(self, objective, image, opt_class='SGD', lr=1.0):
        self.objective = objective
        self.image = image
        self.lr = lr

        self.optimizer = getattr(torch.optim, opt_class)([image], lr=lr)
        self.iteration = 1

    def step(self):
        # The first 10 iterations, we increase the learning rate slowly to full value.
        for group in self.optimizer.param_groups:
            group["lr"] = self.lr * min(self.iteration / 10.0, 1.0) ** 2

        # Each iteration we reset the accumulated gradients and compute the objective.
        self.iteration += 1
        self.optimizer.zero_grad()

        # Let the objective compute the loss and its gradients.
        loss = self.objective(self.image)
        assert not torch.isnan(self.image.grad).any(), f"Gradient is NaN for loss {loss}."

        # Now compute the updates to the image according to the gradients.
        self.optimizer.step()
        assert not torch.isnan(self.image).any(), f"Image is NaN for loss {loss}."

        return loss


class MultiCriticObjective:
    """An `Objective` that defines a problem to be solved by evaluating candidate
    solutions (i.e. images) and returning the computed error.

    This objective evaluates a list of critics to produce a final "loss" that's the sum
    of all the scores returned by the critics.  It's also responsible for computing the
    gradients.
    """

    def __init__(self, encoder, critics):
        self.encoder = encoder
        self.critics = critics

    def __call__(self, image):
        """Main evaluation function that's called by the solver.  Processes the image,
        computes the gradients, and returns the loss.
        """

        # Extract features from image.
        feats = dict(self.encoder.extract(image, [c.get_layers() for c in self.critics]))

        # Apply all the critics one by one.
        scores = []
        for critic in self.critics:
            total = 0.0
            for loss in critic.evaluate(feats):
                total += loss
            scores.append(total)

        # Calculate the final loss and compute the gradients.
        loss = (sum(scores) / len(scores)).mean()
        loss.backward()

        return loss, scores
