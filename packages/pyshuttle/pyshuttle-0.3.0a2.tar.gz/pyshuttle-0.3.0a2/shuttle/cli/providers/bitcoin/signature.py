#!/usr/bin/env python
# coding=utf-8

from base64 import b64encode, b64decode

import json
import sys
import binascii

from shuttle.cli import click
from shuttle.providers.bitcoin.solver \
    import FundSolver, ClaimSolver, RefundSolver
from shuttle.providers.bitcoin.signature \
    import FundSignature, ClaimSignature, RefundSignature

# Bitcoin network.
NETWORK = "mainnet"  # testnet
# Bitcoin transaction version.
VERSION = 2  # 1


@click.command("sign", options_metavar="[OPTIONS]",
               short_help="Select Bitcoin transaction raw signer.")
@click.option("-p", "--private", type=str, required=True, help="Set Bitcoin private key.")
@click.option("-r", "--raw", type=str, required=True, help="Set Bitcoin unsigned transaction raw.")
@click.option("-s", "--secret", type=str, default=None, help="Set secret key.")
@click.option("-v", "--version", type=int, default=VERSION,
              help="Set Bitcoin transaction version.", show_default=True)
def sign(private, raw, secret, version):
    if secret is None:
        secret = str()
    if len(private) != 64:
        click.echo(click.style("Error: {}")
                   .format("invalid bitcoin private key"), err=True)
        sys.exit()

    unsigned_raw = str(raw + "=" * (-len(raw) % 4))
    try:
        transaction = json.loads(b64decode(unsigned_raw.encode()).decode())
    except (binascii.Error, json.decoder.JSONDecodeError) as exception:
        click.echo(click.style("Error: {}")
                   .format("invalid bitcoin unsigned transaction raw"), err=True)
        sys.exit()
    if "type" not in transaction or "network" not in transaction:
        click.echo(click.style("Warning: {}", fg="yellow")
                   .format("there is no type & network provided in bitcoin unsigned transaction raw"), err=True)
        click.echo(click.style("Error: {}")
                   .format("invalid bitcoin unsigned transaction raw"), err=True)
        sys.exit()

    if transaction["type"] == "bitcoin_fund_unsigned":
        # Fund HTLC solver
        fund_solver = FundSolver(private_key=private)
        try:
            # Fund signature
            fund_signature = FundSignature(network=transaction["network"], version=version)
            fund_signature.sign(unsigned_raw=unsigned_raw, solver=fund_solver)
            click.echo(fund_signature.signed_raw())
        except Exception as exception:
            click.echo(click.style("Error: {}").format(str(exception)), err=True)
            sys.exit()

    elif transaction["type"] == "bitcoin_claim_unsigned":
        if secret != str():
            _secret = secret
        elif "secret" not in transaction or transaction["secret"] is None:
            click.echo(click.style("Warning: {}")
                       .format("secret key is empty, use -s or --secret \"Hello Meheret!\""), err=False)
            _secret = str()
        else:
            _secret = transaction["secret"]
        # Claim HTLC solver
        claim_solver = ClaimSolver(
            secret=_secret,
            private_key=private
        )
        try:
            # Claim signature
            claim_signature = ClaimSignature(network=transaction["network"], version=version)
            claim_signature.sign(unsigned_raw=unsigned_raw, solver=claim_solver)
            click.echo(claim_signature.signed_raw())
        except Exception as exception:
            click.echo(click.style("Error: {}").format(str(exception)), err=True)
            sys.exit()

    elif transaction["type"] == "bitcoin_refund_unsigned":
        if secret != str():
            _secret = secret
        elif "secret" not in transaction or transaction["secret"] is None:
            click.echo(click.style("Warning: {}")
                       .format("secret key is empty, use -s or --secret \"Hello Meheret!\""), err=False)
            _secret = str()
        else:
            _secret = transaction["secret"]
        # Refunding HTLC solver
        refund_solver = RefundSolver(
            secret=_secret,
            private_key=private
        )
        try:
            # Refund signature
            refund_signature = RefundSignature(network=transaction["network"], version=version)
            refund_signature.sign(unsigned_raw=unsigned_raw, solver=refund_solver)
            click.echo(refund_signature.signed_raw())
        except Exception as exception:
            click.echo(click.style("Error: {}").format(str(exception)), err=True)
            sys.exit()
