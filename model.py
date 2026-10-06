import torch
import torch.nn as nn


class ResidualDenseBlock_5C(nn.Module):
    def __init__(self, nf, gc=32, bias=True):
        super().__init__()

        self.conv1 = nn.Conv2d(nf, gc, 3, 1, 1, bias=bias)
        self.conv2 = nn.Conv2d(nf + gc * 1, gc, 3, 1, 1, bias=bias)
        self.conv3 = nn.Conv2d(nf + gc * 2, gc, 3, 1, 1, bias=bias)
        self.conv4 = nn.Conv2d(nf + gc * 3, gc, 3, 1, 1, bias=bias)
        self.conv5 = nn.Conv2d(nf + gc * 4, nf, 3, 1, 1, bias=bias)

        self.lrelu = nn.LeakyReLU(0.2, inplace=True)

    def forward(self, x):
        x1 = self.lrelu(self.conv1(x))
        x2 = self.lrelu(self.conv2(torch.cat((x, x1), 1)))
        x3 = self.lrelu(self.conv3(torch.cat((x, x1, x2), 1)))
        x4 = self.lrelu(self.conv4(torch.cat((x, x1, x2, x3), 1)))
        x5 = self.conv5(torch.cat((x, x1, x2, x3, x4), 1))

        return x5 * 0.2 + x


class RRDB(nn.Module):
    def __init__(self, nf, gc=32):
        super().__init__()

        self.rdb1 = ResidualDenseBlock_5C(nf, gc)
        self.rdb2 = ResidualDenseBlock_5C(nf, gc)
        self.rdb3 = ResidualDenseBlock_5C(nf, gc)

    def forward(self, x):
        out = self.rdb1(x)
        out = self.rdb2(out)
        out = self.rdb3(out)

        return out * 0.2 + x


def init_weights(m):
    if isinstance(m, nn.Conv2d):
        nn.init.kaiming_normal_(
            m.weight,
            a=0.2,
            mode="fan_in",
            nonlinearity="leaky_relu"
        )

        if m.bias is not None:
            nn.init.zeros_(m.bias)


class SuperResolver(nn.Module):
    def __init__(
        self,
        in_channels=3,
        out_channels=3,
        num_features=64,
        num_blocks=16,
        scale=4
    ):
        super().__init__()

        self.conv_first = nn.Conv2d(
            in_channels,
            num_features,
            3,
            1,
            1
        )

        self.RRDB_trunk = nn.Sequential(
            *[
                RRDB(num_features, 32)
                for _ in range(num_blocks)
            ]
        )

        self.trunk_conv = nn.Conv2d(
            num_features,
            num_features,
            3,
            1,
            1
        )

        up_layers = []

        for _ in range(int(scale / 2)):
            up_layers += [
                nn.Conv2d(
                    num_features,
                    num_features * 4,
                    3,
                    1,
                    1
                ),
                nn.PixelShuffle(2),
                nn.LeakyReLU(0.2, inplace=True)
            ]

        self.upsampler = nn.Sequential(*up_layers)

        self.conv_seclast = nn.Conv2d(
            num_features,
            num_features,
            3,
            1,
            1
        )

        self.lrelu = nn.LeakyReLU(
            0.2,
            inplace=True
        )

        self.conv_last = nn.Conv2d(
            num_features,
            out_channels,
            3,
            1,
            1
        )

        self.apply(init_weights)

    def forward(self, x):
        feat = self.conv_first(x)

        trunk = self.trunk_conv(
            self.RRDB_trunk(feat)
        )

        feat = feat + trunk * 0.2

        feat = self.upsampler(feat)

        feat = self.lrelu(
            self.conv_seclast(feat)
        )

        out = self.conv_last(feat)

        return out