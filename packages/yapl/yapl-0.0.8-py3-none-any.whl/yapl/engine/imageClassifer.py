import torch
import tensorflow as tf

from ..utils.loss import AverageMeterTorch
from ..utils.accuracy import AverageBinaryAccuracyTorch

class TfEngine:
    def __init_(self, model, dataloader, config):
        self.model = model
        self.dataloader = dataloader
        self.config = config

    def loopengine(self, istraining = True):
        history = []
        for epoch in range(self.config.EPOCHES):
            epoch_loss_avg = tf.keras.metrics.Mean()
            epoch_accuracy_avg = tf.keras.metrics.BinaryAccuracy()

            for it, (data_batch, label_batch) in enumerate(dataset):

                if it%50 == 0:
                    print(it)

                with tf.GradientTape() as tape:
                    output = model(data_batch, training=True)
                    losses = self.config.LOSS(y_true = label_batch, y_pred=output)
                    grads = tape.gradient(losses, model.trainable_variables)
                    self.config.OPTIMIZER.apply_gradients(zip(grads, model.trainable_variables))
                    epoch_loss_avg.update_state(losses)
                    epoch_accuracy_avg.update_state(label_batch, tf.squeeze(output))

            print('Loss: {} | Accuracy: {}'.format(epoch_loss_avg.result(), epoch_accuracy_avg.result()))
            history.append((epoch_loss_avg.result(), epoch_accuracy_avg.result()))
        
        return history

    def fitengine(self, istraining = True):
        model.compile(
            optimizer=self.config.OPTIMIZER, 
            loss=self.config.LOSS, 
            metrics=self.config.ACCURACY
        )
        history = model.fit(
            dataset, 
            epochs=self.config.EPOCHES, 
            steps_per_epoch=(self.config.TOTAL_TRAIN_IMG//self.config.BATCH_SIZE),
    #         callbacks=[
    #             Callbacks().checkpoint_logger(),
    #             Callbacks().tesorboard_logger()
    #         ]
        )

        return history


class TorchEngine:
    def __init_(self, model, dataloader, config):
        self.model = model
        self.dataloader = dataloader
        self.config = config

    def loopengine(self, istraining = True):
        if istraining:
            model.train()
            loss_avg = AverageLossTorch()
            acc_avg = AverageBinaryAccuracyTorch()

            for (data_batch, label_batch) in dataloader:
                print(".", end='')
                data_batch = data_batch.to(self.config.DEVICE, dtype=torch.float)
                label_batch = label_batch.to(self.config.DEVICE, dtype=torch.float)
                
                self.config.OPTIMIZER.zero_grad()
                output = model(data_batch)
                
                losses = self.config.LOSS(output, label_batch.unsqueeze(1))
                losses.backward()
                self.config.OPTIMIZER.step()
                
                loss_avg.update(losses.item(), self.config.BATCH_SIZE)
                acc_avg.update(output, label_batch.unsqueeze(1))
                
                del data_batch
                del label_batch
                
                torch.cuda.empty_cache()

            return loss_avg.avg, acc_avg.avg.item()
        
        else:
