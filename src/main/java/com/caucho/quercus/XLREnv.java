package com.caucho.quercus;

import com.caucho.quercus.env.CliEnv;
import com.caucho.quercus.env.LongValue;
import com.caucho.quercus.env.NullValue;
import com.caucho.quercus.env.Value;
import com.caucho.quercus.page.QuercusPage;
import com.caucho.vfs.WriteStream;

import java.io.IOException;
import java.util.Objects;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 * Created by jdewinne on 5/18/16.
 */
public class XLREnv extends CliEnv {
    private static final Logger log = Logger.getLogger(XLREnv.class.getName());

    public XLREnv(QuercusContext quercus, QuercusPage page, WriteStream out, String[] argv) {
        super(quercus, page, out, argv);
    }

    @Override
    public Value exit(Value msg) {
        if(!msg.isNull() && !(msg instanceof LongValue)) {
            try {
                this.getOut().print(msg.toString());
            } catch (IOException var3) {
                log.log(Level.WARNING, var3.toString(), var3);
            }

            throw new QuercusExitException(msg.toString() + "\n" + this.getStackTraceAsString());
        } else {
            if(!msg.isNull()) {
                // When we get exit code 0
                if (Objects.equals(msg.toString(), "0")) {
                    return NullValue.NULL;
                }
            }
            return this.exit();
        }
    }

    @Override
    public Value exit() {
        throw new QuercusExitException(this.getStackTraceAsString());
    }
}
